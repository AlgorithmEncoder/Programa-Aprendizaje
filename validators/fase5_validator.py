from validators.base_validator import (
    BaseValidator,
    ValidationError
)


class Fase5Validator(BaseValidator):

    def validate(
        self,
        output_json,
        min_preguntas,
        max_preguntas
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

        self._validate_count(
            preguntas,
            min_preguntas,
            max_preguntas
        )

        self._validate_structure(
            preguntas
        )

        self._validate_duplicates(
            preguntas
        )

        self._validate_question_quality(
            preguntas
        )

        return True

    # =========================
    # COUNT
    # =========================

    def _validate_count(
        self,
        preguntas,
        minimum,
        maximum
    ):

        total = len(preguntas)

        if total < minimum:
            self.result.add(
                f"Preguntas insuficientes ({total})"
            )

        if total > maximum:
            self.result.add(
                f"Demasiadas preguntas ({total})"
            )

    # =========================
    # STRUCTURE
    # =========================

    def _validate_structure(
        self,
        preguntas
    ):

        required = [
            "pregunta",
            "respuesta_correcta"
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

    # =========================
    # DUPLICATES
    # =========================

    def _validate_duplicates(
        self,
        preguntas
    ):

        textos = [
            p["pregunta"].strip().lower()
            for p in preguntas
        ]

        self.validate_no_duplicates(
            textos,
            "preguntas"
        )

    # =========================
    # QUALITY
    # =========================

    def _validate_question_quality(
        self,
        preguntas
    ):

        for p in preguntas:

            pregunta = p["pregunta"].strip()
            respuesta = p["respuesta_correcta"].strip()

            if len(pregunta) < 10:

                self.result.add(
                    "Pregunta demasiado corta"
                )

            if respuesta.lower() in pregunta.lower():

                self.result.add(
                    f"La respuesta aparece "
                    f"en la pregunta: {pregunta}"
                )