from validators.base_validator import (
    BaseValidator,
    ValidationError
)


class Fase6Validator(BaseValidator):

    def validate(
        self,
        output_json,
        preguntas_originales,
        respuestas_incorrectas_por_pregunta
    ):
        
        self.result = self.new_result()

        self.require_keys(
            output_json,
            ["preguntas"]
        )

        preguntas = output_json["preguntas"]

        self.require_non_empty_list(
            preguntas,
            "preguntas"
        )

        self._validate_all_questions_present(
            preguntas,
            preguntas_originales
        )

        self._validate_structure(
            preguntas,
            respuestas_incorrectas_por_pregunta
        )

        self._validate_answers(
            preguntas
        )

        self._validate_lengths(
            preguntas
        )

        return True

    # =========================
    # ALL QUESTIONS
    # =========================

    def _validate_all_questions_present(
        self,
        generated,
        originals
    ):

        generated_set = {
            q["pregunta"]
            for q in generated
        }

        original_set = {
            q["pregunta"]
            for q in originals
        }

        if generated_set != original_set:

            self.result.add(
                "Faltan preguntas o existen preguntas extra"
            )

    # =========================
    # STRUCTURE
    # =========================

    def _validate_structure(
        self,
        preguntas,
        expected_count
    ):

        required = [
            "pregunta",
            "respuesta_correcta",
            "respuestas_incorrectas"
        ]

        for p in preguntas:

            self.require_keys(
                p,
                required
            )

            self.require_non_empty_string(
                p["pregunta"],
                "pregunta"
            )

            self.require_non_empty_string(
                p["respuesta_correcta"],
                "respuesta_correcta"
            )

            incorrectas = p[
                "respuestas_incorrectas"
            ]

            if not isinstance(
                incorrectas,
                list
            ):
                self.result.add(
                    "respuestas_incorrectas debe ser lista"
                )

            if len(
                incorrectas
            ) != expected_count:

                self.result.add(
                    "Número incorrecto de distractores"
                )

    # =========================
    # ANSWERS
    # =========================

    def _validate_answers(
        self,
        preguntas
    ):

        for p in preguntas:

            correcta = (
                p["respuesta_correcta"]
                .strip()
                .lower()
            )

            incorrectas = [
                x.strip().lower()
                for x in p["respuestas_incorrectas"]
            ]

            if correcta in incorrectas:

                self.result.add(
                    "Respuesta correcta incluida "
                    "entre las incorrectas"
                )

            if len(
                incorrectas
            ) != len(set(incorrectas)):

                self.result.add(
                    "Distractores duplicados"
                )

            for respuesta in incorrectas:

                if not respuesta:

                    self.result.add(
                        "Respuesta vacía"
                    )

    # =========================
    # LENGTHS
    # =========================

    def _validate_lengths(
        self,
        preguntas
    ):

        for p in preguntas:

            correcta = len(
                p["respuesta_correcta"]
            )

            for incorrecta in p[
                "respuestas_incorrectas"
            ]:

                longitud = len(
                    incorrecta
                )

                if longitud < max(
                    1,
                    correcta * 0.3
                ):
                    self.result.add(
                        "Distractor demasiado corto"
                    )

                if longitud > (
                    correcta * 3
                ):
                    self.result.add(
                        "Distractor demasiado largo"
                    )