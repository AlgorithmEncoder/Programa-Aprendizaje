from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Callable

import config.settings as settings

from ai.generators.fase1_generator import Fase1Generator
from ai.generators.fase2_generator import Fase2Generator
from ai.generators.fase3_generator import Fase3Generator
from ai.generators.fase4_generator import Fase4Generator
from ai.generators.fase5_generator import Fase5Generator
from ai.generators.fase6_generator import Fase6Generator

from database.repositories.bloques_repository import BloquesRepository
from database.repositories.conocimientos_repository import ConocimientosRepository
from database.repositories.generaciones_repository import GeneracionesRepository
from database.repositories.preguntas_repository import PreguntasRepository
from database.repositories.respuestas_repository import RespuestasRepository
from database.repositories.temarios_repository import TemariosRepository
from database.repositories.temas_repository import TemasRepository

from services.tema_service import TemaService

from utils.logger import get_logger

from validators.fase1_validator import Fase1Validator
from validators.fase2_validator import Fase2Validator
from validators.fase4_validator import Fase4Validator
from validators.fase5_validator import Fase5Validator
from validators.fase6_validator import Fase6Validator


class GenerationService:
    """
    Orquestador principal del flujo de generación educativa.

    Responsabilidades:
    - ejecutar fases IA,
    - validar respuestas,
    - dejar preparado el sistema para reviews futuras,
    - persistir resultados en BD,
    - registrar el histórico en generaciones.
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

        self.tema_service = TemaService()

        self.temas_repo = TemasRepository()
        self.bloques_repo = BloquesRepository()
        self.temarios_repo = TemariosRepository()
        self.conocimientos_repo = ConocimientosRepository()
        self.preguntas_repo = PreguntasRepository()
        self.respuestas_repo = RespuestasRepository()
        self.generaciones_repo = GeneracionesRepository()

        self.fase1_generator = Fase1Generator()
        self.fase2_generator = Fase2Generator()
        self.fase3_generator = Fase3Generator()
        self.fase4_generator = Fase4Generator()
        self.fase5_generator = Fase5Generator()
        self.fase6_generator = Fase6Generator()

        # Registro preparado para reviews futuras.
        # Ejemplo:
        # self.reviewers["fase1"] = [reviewer_1, reviewer_2]
        self.reviewers: dict[str, list[Callable[[dict[str, Any], dict[str, Any]], dict[str, Any] | None]]] = {}

    # =========================================================
    # API PÚBLICA
    # =========================================================

    def generate_topic(
        self,
        tema_nombre: str,
        descripcion: str | None = None,
        numero_bloques: int | None = None,
    ) -> dict[str, Any]:
        """
        Ejecuta el pipeline completo para un tema.

        Devuelve un resumen estructurado con el tema, bloques y
        elementos creados en cada fase.
        """
        self._ensure_pipeline_enabled()

        descripcion_final = descripcion or ""
        self.logger.info("Iniciando generación completa del tema: %s", tema_nombre)

        tema = self.tema_service.get_or_create(
            nombre=tema_nombre,
            descripcion=descripcion
        )

        resumen: dict[str, Any] = {
            "tema": self._model_to_dict(tema),
            "bloques": [],
        }

        # -----------------------------------------------------
        # FASE 1 - ESQUEMATIZACIÓN
        # -----------------------------------------------------
        fase1_output = self._execute_phase(
            phase_name="fase1",
            tema_nombre=tema_nombre,
            input_data={
                "tema": tema_nombre,
                "descripcion": descripcion_final,
            },
            generator_callable=lambda: self.fase1_generator.generate(
                tema=tema_nombre,
                descripcion=descripcion
            ),
            validator_callable=lambda output: self._validate_fase1_output(output),
        )

        conceptos = fase1_output["conceptos"]

        # -----------------------------------------------------
        # FASE 2 - AGRUPACIÓN
        # -----------------------------------------------------
        total_bloques = numero_bloques or getattr(settings, "DEFAULT_NUM_BLOQUES", 10)

        fase2_output = self._execute_phase(
            phase_name="fase2",
            tema_nombre=tema_nombre,
            input_data={
                "conceptos": conceptos,
                "numero_bloques": total_bloques,
            },
            generator_callable=lambda: self.fase2_generator.generate(
                conceptos=conceptos,
                numero_bloques=total_bloques
            ),
            validator_callable=lambda output: self._validate_fase2_output(
                output=output,
                conceptos_originales=conceptos,
                numero_bloques=total_bloques
            ),
            persistence_callable=lambda output: self._save_bloques_for_theme(
                tema_id=tema.id,
                bloques_json=output["bloques"]
            ),
        )

        bloques = fase2_output["bloques"]

        # -----------------------------------------------------
        # FASES 3 a 6 - POR BLOQUE
        # -----------------------------------------------------
        for bloque_json in bloques:
            bloque_numero = bloque_json["numero"]
            bloque_id = self._get_bloque_id(tema_id=tema.id, bloque_numero=bloque_numero)

            bloque_resumen: dict[str, Any] = {
                "numero": bloque_numero,
                "bloque": bloque_json,
                "temarios": [],
                "conocimientos": [],
                "preguntas": [],
            }

            # FASE 3 - TEMARIO
            fase3_output = self._execute_phase(
                phase_name="fase3",
                tema_nombre=tema_nombre,
                numero_bloque=bloque_numero,
                input_data={
                    "tema": tema_nombre,
                    "descripcion_tema": descripcion_final,
                    "bloque": bloque_json,
                    "min_temarios": getattr(settings, "MIN_TEMARIOS_PER_BLOCK", 7),
                    "max_temarios": getattr(settings, "MAX_TEMARIOS_PER_BLOCK", 10),
                },
                generator_callable=lambda: self.fase3_generator.generate(
                    tema=tema_nombre,
                    descripcion_tema=descripcion,
                    bloque=bloque_json,
                    min_temarios=getattr(settings, "MIN_TEMARIOS_PER_BLOCK", 7),
                    max_temarios=getattr(settings, "MAX_TEMARIOS_PER_BLOCK", 10),
                ),
                validator_callable=lambda output: self._validate_fase3_output(output=output),
                persistence_callable=lambda output: self._save_temarios_for_block(
                    bloque_id=bloque_id,
                    temarios_json=output["temarios"]
                ),
            )

            temarios = fase3_output["temarios"]
            temarios_payload = [
                {
                    "id": t.get("id"),
                    "titulo": t["titulo"],
                    "contenido": t["contenido"],
                }
                for t in temarios
            ]

            # FASE 4 - CONOCIMIENTOS
            fase4_output = self._execute_phase(
                phase_name="fase4",
                tema_nombre=tema_nombre,
                numero_bloque=bloque_numero,
                input_data={
                    "tema": tema_nombre,
                    "descripcion_tema": descripcion_final,
                    "bloque": bloque_json,
                    "temarios": temarios_payload,
                    "tipos_relacion_permitidos": getattr(settings, "TIPOS_RELACION_PERMITIDOS", []),
                    "min_conocimientos": getattr(settings, "MIN_CONOCIMIENTOS", 20),
                    "max_conocimientos": getattr(settings, "MAX_CONOCIMIENTOS", 50),
                },
                generator_callable=lambda: self.fase4_generator.generate(
                    tema=tema_nombre,
                    descripcion_tema=descripcion,
                    bloque=bloque_json,
                    temarios=temarios_payload,
                    tipos_relacion_permitidos=getattr(settings, "TIPOS_RELACION_PERMITIDOS", []),
                    min_conocimientos=getattr(settings, "MIN_CONOCIMIENTOS", 20),
                    max_conocimientos=getattr(settings, "MAX_CONOCIMIENTOS", 50),
                ),
                validator_callable=lambda output: self._validate_fase4_output(
                    output=output,
                    tipos_relacion_permitidos=getattr(settings, "TIPOS_RELACION_PERMITIDOS", []),
                    min_conocimientos=getattr(settings, "MIN_CONOCIMIENTOS", 20),
                    max_conocimientos=getattr(settings, "MAX_CONOCIMIENTOS", 50),
                ),
                persistence_callable=lambda output: self._save_conocimientos_for_block(
                    bloque_id=bloque_id,
                    conocimientos_json=output["conocimientos"]
                ),
            )

            conocimientos = fase4_output["conocimientos"]
            conocimientos_payload = [
                {
                    "id": c.get("id"),
                    "temario_id": c.get("temario_id"),
                    "concepto_a": c["concepto_a"],
                    "tipo_relacion": c["tipo_relacion"],
                    "relacion": c["relacion"],
                    "concepto_b": c["concepto_b"],
                    "explicacion": c.get("explicacion"),
                }
                for c in conocimientos
            ]

            # FASE 5 - PREGUNTAS
            fase5_output = self._execute_phase(
                phase_name="fase5",
                tema_nombre=tema_nombre,
                numero_bloque=bloque_numero,
                input_data={
                    "tema": tema_nombre,
                    "descripcion_tema": descripcion_final,
                    "bloque": bloque_json,
                    "conocimientos": conocimientos_payload,
                    "min_preguntas": getattr(settings, "MIN_PREGUNTAS", 20),
                    "max_preguntas": getattr(settings, "MAX_PREGUNTAS", 50),
                },
                generator_callable=lambda: self.fase5_generator.generate(
                    tema=tema_nombre,
                    descripcion_tema=descripcion,
                    bloque=bloque_json,
                    conocimientos=conocimientos_payload,
                    min_preguntas=getattr(settings, "MIN_PREGUNTAS", 20),
                    max_preguntas=getattr(settings, "MAX_PREGUNTAS", 50),
                ),
                validator_callable=lambda output: self._validate_fase5_output(
                    output=output,
                    min_preguntas=getattr(settings, "MIN_PREGUNTAS", 20),
                    max_preguntas=getattr(settings, "MAX_PREGUNTAS", 50),
                    conocimientos_originales=conocimientos_payload,
                ),
                persistence_callable=lambda output: self._save_questions_for_block(
                    bloque_id=bloque_id,
                    conocimientos_payload=conocimientos_payload,
                    preguntas_json=output["preguntas"]
                ),
            )

            preguntas = fase5_output["preguntas"]
            preguntas_payload = [
                {
                    "id": p.get("id"),
                    "conocimiento_id": p.get("conocimiento_id"),
                    "pregunta": p["pregunta"],
                    "respuesta_correcta": p["respuesta_correcta"],
                }
                for p in preguntas
            ]

            # FASE 6 - RESPUESTAS INCORRECTAS
            fase6_output = self._execute_phase(
                phase_name="fase6",
                tema_nombre=tema_nombre,
                numero_bloque=bloque_numero,
                input_data={
                    "tema": tema_nombre,
                    "descripcion_tema": descripcion_final,
                    "bloque": bloque_json,
                    "preguntas": preguntas_payload,
                    "respuestas_incorrectas_por_pregunta": getattr(
                        settings,
                        "RESPUESTAS_INCORRECTAS_POR_PREGUNTA",
                        3,
                    ),
                    "dificultad_distractores": getattr(
                        settings,
                        "PROFUNDIDAD_DEFAULT",
                        "media",
                    ),
                },
                generator_callable=lambda: self.fase6_generator.generate(
                    tema=tema_nombre,
                    descripcion_tema=descripcion,
                    bloque=bloque_json,
                    preguntas=preguntas_payload,
                    respuestas_incorrectas_por_pregunta=getattr(
                        settings,
                        "RESPUESTAS_INCORRECTAS_POR_PREGUNTA",
                        3,
                    ),
                    dificultad_distractores=getattr(
                        settings,
                        "PROFUNDIDAD_DEFAULT",
                        "media",
                    ),
                ),
                validator_callable=lambda output: self._validate_fase6_output(
                    output=output,
                    preguntas_originales=preguntas_payload,
                    respuestas_incorrectas_por_pregunta=getattr(
                        settings,
                        "RESPUESTAS_INCORRECTAS_POR_PREGUNTA",
                        3,
                    ),
                ),
                persistence_callable=lambda output: self._save_incorrect_answers_for_block(
                    preguntas_payload=preguntas_payload,
                    preguntas_json=output["preguntas"]
                ),
            )

            bloque_resumen["temarios"] = temarios
            bloque_resumen["conocimientos"] = conocimientos
            bloque_resumen["preguntas"] = fase6_output["preguntas"]
            resumen["bloques"].append(bloque_resumen)

        self.logger.info("Generación completada correctamente: %s", tema_nombre)
        return resumen

    # =========================================================
    # PIPELINE GENÉRICO
    # =========================================================

    def _execute_phase(
        self,
        phase_name: str,
        tema_nombre: str,
        input_data: dict[str, Any],
        generator_callable: Callable[[], dict[str, Any]],
        validator_callable: Callable[[dict[str, Any]], None] | None = None,
        persistence_callable: Callable[[dict[str, Any]], Any] | None = None,
        numero_bloque: int | None = None,
        subfase: str | None = None,
    ) -> dict[str, Any]:
        """
        Ejecuta una fase completa:
        1. registra la generación,
        2. llama a la IA,
        3. guarda salida y uso,
        4. ejecuta reviews futuras si existen,
        5. valida,
        6. persiste el resultado en BD,
        7. marca la generación como completada.
        """
        max_retries = getattr(settings, "MAX_RETRIES_PER_PHASE", 3)

        last_error: Exception | None = None

        for attempt in range(1, max_retries + 1):
            generacion = self.generaciones_repo.create(
                tema_nombre=tema_nombre,
                fase=phase_name,
                estado="ejecutando",
                subfase=subfase,
                numero_bloque=numero_bloque,
                json_entrada=input_data,
                prompt=None,
                modelo=getattr(settings, "OPENAI_MODEL", None),
            )

            try:
                self.logger.info(
                    "Ejecutando %s (intento %s/%s)",
                    phase_name,
                    attempt,
                    max_retries
                )

                ai_result = generator_callable()
                output_data = ai_result["content"]

                # Guardamos primero el output crudo para trazabilidad.
                self.generaciones_repo.save_usage(
                    generacion.id,
                    ai_result.get("tokens_input", 0),
                    ai_result.get("tokens_output", 0),
                    ai_result.get("cost_estimated", 0.0),
                )
                self.generaciones_repo.save_output(
                    generacion.id,
                    output_data
                )

                # Hook para revisiones futuras. Si corrigen el output, se revalidará.
                self._run_reviews(
                    phase_name=phase_name,
                    input_data=input_data,
                    output_data=output_data
                )

                if validator_callable is not None:
                    validator_callable(output_data)

                # Guardamos el output final, ya revisado/validado.
                self.generaciones_repo.save_output(
                    generacion.id,
                    output_data
                )

                if persistence_callable is not None:
                    persistence_callable(output_data)

                self.generaciones_repo.update_estado(
                    generacion.id,
                    "completado"
                )

                return output_data

            except Exception as exc:
                last_error = exc

                try:
                    self.generaciones_repo.mark_error(
                        generacion.id,
                        str(exc)
                    )
                except Exception:
                    self.logger.exception(
                        "No se pudo registrar el error de %s en BD",
                        phase_name
                    )

                self.logger.exception(
                    "Error en %s (intento %s/%s): %s",
                    phase_name,
                    attempt,
                    max_retries,
                    exc
                )

                if attempt >= max_retries:
                    raise

        raise last_error if last_error is not None else RuntimeError(
            f"No se pudo completar la fase {phase_name}"
        )

    # =========================================================
    # VALIDACIONES
    # =========================================================

    def _validate_fase1_output(self, output: dict[str, Any]) -> None:
        validator = Fase1Validator()
        validator.validate(output)
        self._ensure_validation_passed(validator, "fase1")

    def _validate_fase2_output(
        self,
        output: dict[str, Any],
        conceptos_originales: list[dict[str, Any]],
        numero_bloques: int,
    ) -> None:
        validator = Fase2Validator()
        validator.validate(
            output_json=output,
            conceptos_originales=conceptos_originales,
            numero_bloques=numero_bloques,
        )
        self._ensure_validation_passed(validator, "fase2")

    def _validate_fase3_output(self, output: dict[str, Any]) -> None:
        errors: list[str] = []

        if "temarios" not in output:
            errors.append("Falta la clave obligatoria: temarios")
        else:
            temarios = output["temarios"]
            if not isinstance(temarios, list) or len(temarios) == 0:
                errors.append("temarios debe ser una lista no vacía")
            else:
                min_temarios = getattr(settings, "MIN_TEMARIOS_PER_BLOCK", 7)
                max_temarios = getattr(settings, "MAX_TEMARIOS_PER_BLOCK", 10)

                if len(temarios) < min_temarios:
                    errors.append(f"Temarios insuficientes ({len(temarios)})")
                if len(temarios) > max_temarios:
                    errors.append(f"Demasiados temarios ({len(temarios)})")

                for idx, temario in enumerate(temarios, start=1):
                    if not isinstance(temario, dict):
                        errors.append(f"Temario inválido en posición {idx}")
                        continue

                    if not str(temario.get("titulo", "")).strip():
                        errors.append(f"Falta o está vacío el título del temario {idx}")

                    if not str(temario.get("contenido", "")).strip():
                        errors.append(f"Falta o está vacío el contenido del temario {idx}")

        if errors:
            raise ValueError("Validación fase3 fallida:\n- " + "\n- ".join(errors))

    def _validate_fase4_output(
        self,
        output: dict[str, Any],
        tipos_relacion_permitidos: list[str],
        min_conocimientos: int,
        max_conocimientos: int,
    ) -> None:
        validator = Fase4Validator()
        validator.validate(
            output_json=output,
            tipos_relacion_permitidos=tipos_relacion_permitidos,
            min_conocimientos=min_conocimientos,
            max_conocimientos=max_conocimientos,
        )
        self._ensure_validation_passed(validator, "fase4")

    def _validate_fase5_output(
        self,
        output: dict[str, Any],
        min_preguntas: int,
        max_preguntas: int,
        conocimientos_originales: list[dict[str, Any]],
    ) -> None:
        validator = Fase5Validator()
        validator.validate(
            output_json=output,
            min_preguntas=min_preguntas,
            max_preguntas=max_preguntas,
        )
        self._ensure_validation_passed(validator, "fase5")

        self._ensure_questions_can_be_mapped_to_knowledge(
            preguntas=output.get("preguntas", []),
            conocimientos_originales=conocimientos_originales,
        )

    def _validate_fase6_output(
        self,
        output: dict[str, Any],
        preguntas_originales: list[dict[str, Any]],
        respuestas_incorrectas_por_pregunta: int,
    ) -> None:
        validator = Fase6Validator()
        validator.validate(
            output_json=output,
            preguntas_originales=preguntas_originales,
            respuestas_incorrectas_por_pregunta=respuestas_incorrectas_por_pregunta,
        )
        self._ensure_validation_passed(validator, "fase6")

    def _ensure_validation_passed(self, validator: Any, phase_name: str) -> None:
        """
        Convierte el resultado interno del validador en una excepción útil.
        """
        result = getattr(validator, "result", None)
        if result is None:
            return

        valid = getattr(result, "valid", True)
        errors = getattr(result, "errors", [])

        if valid is False or errors:
            formatted_errors = (
                "\n- ".join(str(e) for e in errors)
                if errors
                else "Error de validación desconocido"
            )
            raise ValueError(
                f"Validación fallida en {phase_name}:\n- {formatted_errors}"
            )

    def _ensure_questions_can_be_mapped_to_knowledge(
        self,
        preguntas: list[dict[str, Any]],
        conocimientos_originales: list[dict[str, Any]],
    ) -> None:
        """
        Fase 5 ya debe devolver una referencia al conocimiento de origen.
        Esta validación asegura que no se generen preguntas huérfanas.
        """
        index_by_id = {
            c.get("id"): c
            for c in conocimientos_originales
            if c.get("id") is not None
        }

        lookup_by_tuple = {
            (
                str(c.get("concepto_a", "")).strip().lower(),
                str(c.get("relacion", "")).strip().lower(),
                str(c.get("concepto_b", "")).strip().lower(),
            ): c
            for c in conocimientos_originales
        }

        errores: list[str] = []

        for pregunta in preguntas:
            conocimiento = self._resolve_conocimiento_for_question(
                pregunta=pregunta,
                index_by_id=index_by_id,
                lookup_by_tuple=lookup_by_tuple,
            )
            if conocimiento is None:
                errores.append(
                    f"No se pudo asociar la pregunta con un conocimiento: {pregunta.get('pregunta')}"
                )

        if errores:
            raise ValueError("Validación fase5 fallida:\n- " + "\n- ".join(errores))

    def _resolve_conocimiento_for_question(
        self,
        pregunta: dict[str, Any],
        index_by_id: dict[Any, dict[str, Any]],
        lookup_by_tuple: dict[tuple[str, str, str], dict[str, Any]],
    ) -> dict[str, Any] | None:
        """
        Soporta varias formas de referencia para que la fase 5 sea flexible:
        - conocimiento_id
        - conocimiento -> {id: ...}
        - concepto_a / relacion / concepto_b
        """
        if pregunta.get("conocimiento_id") is not None:
            return index_by_id.get(pregunta["conocimiento_id"])

        conocimiento_ref = pregunta.get("conocimiento")
        if isinstance(conocimiento_ref, dict) and conocimiento_ref.get("id") is not None:
            encontrado = index_by_id.get(conocimiento_ref["id"])
            if encontrado is not None:
                return encontrado

        clave = (
            str(pregunta.get("concepto_a", "")).strip().lower(),
            str(pregunta.get("relacion", "")).strip().lower(),
            str(pregunta.get("concepto_b", "")).strip().lower(),
        )
        if clave != ("", "", ""):
            return lookup_by_tuple.get(clave)

        return None

    # =========================================================
    # PERSISTENCIA
    # =========================================================

    def _save_bloques_for_theme(
        self,
        tema_id: int,
        bloques_json: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        bloque_records: list[dict[str, Any]] = []

        for bloque_json in bloques_json:
            bloque = self.bloques_repo.create(
                tema_id=tema_id,
                numero=bloque_json["numero"],
                titulo=bloque_json["titulo"],
                descripcion=bloque_json.get("descripcion"),
            )
            bloque_records.append({
                "id": bloque.id,
                "numero": bloque.numero,
                "titulo": bloque.titulo,
                "descripcion": bloque.descripcion,
            })

        return bloque_records

    def _save_temarios_for_block(
        self,
        bloque_id: int,
        temarios_json: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        temarios_guardados: list[dict[str, Any]] = []

        for orden, temario_json in enumerate(temarios_json, start=1):
            temario = self.temarios_repo.create(
                bloque_id=bloque_id,
                titulo=temario_json.get("titulo"),
                contenido=temario_json["contenido"],
                orden=orden,
            )
            temarios_guardados.append({
                "id": temario.id,
                "bloque_id": temario.bloque_id,
                "titulo": temario.titulo,
                "contenido": temario.contenido,
                "orden": temario.orden,
            })

        return temarios_guardados

    def _save_conocimientos_for_block(
        self,
        bloque_id: int,
        conocimientos_json: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        conocimientos_guardados: list[dict[str, Any]] = []

        for orden, conocimiento_json in enumerate(conocimientos_json, start=1):
            conocimiento = self.conocimientos_repo.create(
                bloque_id=bloque_id,
                temario_id=conocimiento_json.get("temario_id"),
                concepto_a=conocimiento_json["concepto_a"],
                tipo_relacion=conocimiento_json["tipo_relacion"],
                relacion=conocimiento_json["relacion"],
                concepto_b=conocimiento_json["concepto_b"],
                explicacion=conocimiento_json.get("explicacion"),
                nivel_dificultad=conocimiento_json.get("nivel_dificultad", 1),
                orden_aprendizaje=conocimiento_json.get("orden_aprendizaje", orden),
            )
            conocimientos_guardados.append({
                "id": conocimiento.id,
                "bloque_id": conocimiento.bloque_id,
                "temario_id": conocimiento.temario_id,
                "concepto_a": conocimiento.concepto_a,
                "tipo_relacion": conocimiento.tipo_relacion,
                "relacion": conocimiento.relacion,
                "concepto_b": conocimiento.concepto_b,
                "explicacion": conocimiento.explicacion,
                "nivel_dificultad": conocimiento.nivel_dificultad,
                "orden_aprendizaje": conocimiento.orden_aprendizaje,
            })

        return conocimientos_guardados

    def _save_questions_for_block(
        self,
        bloque_id: int,
        conocimientos_payload: list[dict[str, Any]],
        preguntas_json: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Guarda preguntas y su respuesta correcta.
        La asociación con conocimiento_id se intenta resolver por:
        - conocimiento_id
        - conocimiento.id
        - (concepto_a, relacion, concepto_b)
        """
        preguntas_guardadas: list[dict[str, Any]] = []

        lookup_by_id = {
            c.get("id"): c
            for c in conocimientos_payload
            if c.get("id") is not None
        }

        lookup_by_tuple = {
            (
                str(c.get("concepto_a", "")).strip().lower(),
                str(c.get("relacion", "")).strip().lower(),
                str(c.get("concepto_b", "")).strip().lower(),
            ): c
            for c in conocimientos_payload
        }

        for pregunta_json in preguntas_json:
            conocimiento = self._resolve_conocimiento_for_question(
                pregunta=pregunta_json,
                index_by_id=lookup_by_id,
                lookup_by_tuple=lookup_by_tuple,
            )

            if conocimiento is None:
                raise ValueError(
                    f"No se pudo resolver el conocimiento de la pregunta: {pregunta_json.get('pregunta')}"
                )

            pregunta = self.preguntas_repo.create(
                conocimiento_id=conocimiento["id"],
                tipo="multiple_choice",
                pregunta=pregunta_json["pregunta"],
            )

            self.respuestas_repo.create(
                pregunta_id=pregunta.id,
                texto=pregunta_json["respuesta_correcta"],
                correcta=True,
            )

            preguntas_guardadas.append({
                "id": pregunta.id,
                "conocimiento_id": pregunta.conocimiento_id,
                "tipo": pregunta.tipo,
                "pregunta": pregunta.pregunta,
                "respuesta_correcta": pregunta_json["respuesta_correcta"],
            })

        return preguntas_guardadas

    def _save_incorrect_answers_for_block(
        self,
        preguntas_payload: list[dict[str, Any]],
        preguntas_json: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Añade distractores a las preguntas ya creadas.
        """
        preguntas_by_text = {
            p["pregunta"]: p
            for p in preguntas_payload
        }

        distractores_guardados: list[dict[str, Any]] = []

        for pregunta_json in preguntas_json:
            pregunta_texto = pregunta_json["pregunta"]
            pregunta_guardada = preguntas_by_text.get(pregunta_texto)

            if pregunta_guardada is None:
                raise ValueError(
                    f"No se encontró la pregunta para guardar distractores: {pregunta_texto}"
                )

            for distractor in pregunta_json["respuestas_incorrectas"]:
                respuesta = self.respuestas_repo.create(
                    pregunta_id=pregunta_guardada["id"],
                    texto=distractor,
                    correcta=False,
                )
                distractores_guardados.append({
                    "id": respuesta.id,
                    "pregunta_id": respuesta.pregunta_id,
                    "texto": respuesta.texto,
                    "correcta": respuesta.correcta,
                })

        return distractores_guardados

    # =========================================================
    # REVIEWS FUTURAS
    # =========================================================

    def _run_reviews(
        self,
        phase_name: str,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
    ) -> None:
        """
        Punto de extensión para reviews IA futuras.

        Por ahora:
        - si no hay reviews configuradas, no hace nada;
        - si hay callbacks registrados en self.reviewers, los ejecuta.
        """
        reviews_enabled = getattr(settings, "ENABLE_REVIEWS", False)
        reviews_per_phase = getattr(settings, "REVIEWS_PER_PHASE", {})

        cantidad = int(reviews_per_phase.get(phase_name, 0) or 0)
        if not reviews_enabled or cantidad <= 0:
            return

        callbacks = self.reviewers.get(phase_name, [])
        if not callbacks:
            self.logger.info(
                "Reviews activadas para %s pero aún no hay revisores registrados.",
                phase_name,
            )
            return

        for i in range(min(cantidad, len(callbacks))):
            callback = callbacks[i]
            reviewed = callback(input_data, output_data)

            # Si el revisor devuelve una versión corregida, la adoptamos.
            if isinstance(reviewed, dict):
                output_data.clear()
                output_data.update(reviewed)

    # =========================================================
    # HELPERS
    # =========================================================

    def _ensure_pipeline_enabled(self) -> None:
        required_phases = [
            ("ENABLE_PHASE_1", "fase1"),
            ("ENABLE_PHASE_2", "fase2"),
            ("ENABLE_PHASE_3", "fase3"),
            ("ENABLE_PHASE_4", "fase4"),
            ("ENABLE_PHASE_5", "fase5"),
            ("ENABLE_PHASE_6", "fase6"),
        ]

        disabled = [
            phase_name
            for setting_name, phase_name in required_phases
            if not getattr(settings, setting_name, True)
        ]

        if disabled:
            raise RuntimeError(
                "El pipeline no puede ejecutarse porque hay fases desactivadas: "
                + ", ".join(disabled)
            )

    def _get_bloque_id(self, tema_id: int, bloque_numero: int) -> int:
        bloque = self.bloques_repo.get_by_tema_and_numero(
            tema_id=tema_id,
            numero=bloque_numero,
        )
        if bloque is None:
            raise ValueError(
                f"No se encontró el bloque {bloque_numero} para el tema_id={tema_id}"
            )
        return bloque.id

    def _model_to_dict(self, obj: Any) -> Any:
        if obj is None:
            return None
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, list):
            return [self._model_to_dict(item) for item in obj]
        if isinstance(obj, dict):
            return {k: self._model_to_dict(v) for k, v in obj.items()}
        return obj
