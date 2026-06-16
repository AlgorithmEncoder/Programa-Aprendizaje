from validators.base_validator import (
    BaseValidator,
    ValidationError
)


class Fase3Validator(BaseValidator):

    def validate(
        self,
        output_json,
        bloque,
        fragmentos_deseados,
        min_total_chars=3000
    ):
        
        self.result = self.new_result()

        self.require_keys(
            output_json,
            ["temarios"]
        )

        temarios = output_json["temarios"]

        self.require_non_empty_list(
            temarios,
            "temarios"
        )

        self._validate_temarios(
            temarios
        )

        self._validate_titles(
            temarios
        )

        self._validate_fragment_count(
            temarios,
            fragmentos_deseados
        )

        self._validate_length(
            temarios,
            min_total_chars
        )

        self._validate_concepts_coverage(
            temarios,
            bloque
        )

        return True

    def _validate_temarios(
        self,
        temarios
    ):
        for t in temarios:

            self.require_keys(
                t,
                [
                    "titulo",
                    "contenido"
                ]
            )

            self.require_non_empty_string(
                t["titulo"],
                "titulo"
            )

            self.require_non_empty_string(
                t["contenido"],
                "contenido"
            )

    def _validate_titles(
        self,
        temarios
    ):
        self.validate_no_duplicates(
            [t["titulo"] for t in temarios],
            "titulos"
        )

    def _validate_fragment_count(
        self,
        temarios,
        desired
    ):
        if abs(len(temarios) - desired) > 2:
            self.result.add(
                "Número de fragmentos incorrecto"
            )

    def _validate_length(
        self,
        temarios,
        minimum
    ):
        total = sum(
            len(t["contenido"])
            for t in temarios
        )

        if total < minimum:
            self.result.add(
                "Contenido insuficiente"
            )

    def _validate_concepts_coverage(
        self,
        temarios,
        bloque
    ):
        text = " ".join(
            t["contenido"]
            for t in temarios
        ).lower()

        for concepto in bloque["conceptos"]:

            if concepto.lower() not in text:
                self.result.add(
                    f"Concepto ausente: {concepto}"
                )