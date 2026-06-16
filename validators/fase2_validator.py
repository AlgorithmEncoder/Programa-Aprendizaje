from validators.base_validator import (
    BaseValidator,
    ValidationError
)


class Fase2Validator(BaseValidator):

    def validate(
        self,
        output_json,
        conceptos_originales,
        numero_bloques
    ):

        self._validate_root(
            output_json,
            numero_bloques
        )
        
        self.result = self.new_result()

        bloques = output_json["bloques"]

        self._validate_blocks(bloques)

        self._validate_concepts_assignment(
            bloques,
            conceptos_originales
        )

        self._validate_dependencies_order(
            bloques,
            conceptos_originales
        )

        return True

    # =========================

    def _validate_root(
        self,
        data,
        numero_bloques
    ):
        self.require_keys(
            data,
            ["bloques"]
        )

        bloques = data["bloques"]

        if len(bloques) != numero_bloques:
            self.result.add(
                "Número incorrecto de bloques"
            )

    def _validate_blocks(
        self,
        bloques
    ):
        expected_numbers = list(
            range(
                1,
                len(bloques) + 1
            )
        )

        real_numbers = []

        for bloque in bloques:

            self.require_keys(
                bloque,
                [
                    "numero",
                    "titulo",
                    "descripcion",
                    "conceptos"
                ]
            )

            self.require_non_empty_string(
                bloque["titulo"],
                "titulo"
            )

            self.require_non_empty_list(
                bloque["conceptos"],
                "conceptos"
            )

            real_numbers.append(
                bloque["numero"]
            )

        if real_numbers != expected_numbers:
            self.result.add(
                "Bloques no consecutivos"
            )

    def _validate_concepts_assignment(
        self,
        bloques,
        conceptos_originales
    ):
        originales = {
            c["nombre"]
            for c in conceptos_originales
        }

        usados = []

        for bloque in bloques:
            usados.extend(
                bloque["conceptos"]
            )

        if set(usados) != originales:
            self.result.add(
                "No coinciden conceptos"
            )

        self.validate_no_duplicates(
            usados,
            "conceptos agrupados"
        )

    def _validate_dependencies_order(
        self,
        bloques,
        conceptos_originales
    ):
        concept_block = {}

        for bloque in bloques:
            for c in bloque["conceptos"]:
                concept_block[c] = bloque["numero"]

        for concepto in conceptos_originales:

            actual = concept_block[
                concepto["nombre"]
            ]

            for dep in concepto["depende_de"]:

                dep_block = concept_block[dep]

                if dep_block > actual:
                    self.result.add(
                        f"Dependencia inválida: "
                        f"{concepto['nombre']}"
                    )