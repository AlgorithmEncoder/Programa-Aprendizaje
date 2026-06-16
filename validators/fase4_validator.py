from validators.base_validator import (
    BaseValidator,
    ValidationError
)


class Fase4Validator(BaseValidator):

    def validate(
        self,
        output_json,
        tipos_relacion_permitidos,
        min_conocimientos,
        max_conocimientos
    ):
        
        self.result = self.new_result()

        self.require_keys(
            output_json,
            ["conocimientos"]
        )

        conocimientos = output_json["conocimientos"]

        self.require_non_empty_list(
            conocimientos,
            "conocimientos"
        )

        self._validate_count(
            conocimientos,
            min_conocimientos,
            max_conocimientos
        )

        self._validate_structure(
            conocimientos
        )

        self._validate_relation_types(
            conocimientos,
            tipos_relacion_permitidos
        )

        self._validate_duplicates(
            conocimientos
        )

        self._validate_explanations(
            conocimientos
        )

        self._validate_contradictions(
            conocimientos
        )

        return True

    # =========================
    # COUNT
    # =========================

    def _validate_count(
        self,
        conocimientos,
        minimum,
        maximum
    ):
        count = len(conocimientos)

        if count < minimum:
            self.result.add(
                f"Conocimientos insuficientes ({count})"
            )

        if count > maximum:
            self.result.add(
                f"Demasiados conocimientos ({count})"
            )

    # =========================
    # STRUCTURE
    # =========================

    def _validate_structure(
        self,
        conocimientos
    ):

        required = [
            "concepto_a",
            "tipo_relacion",
            "relacion",
            "concepto_b",
            "explicacion"
        ]

        for c in conocimientos:

            self.require_keys(
                c,
                required
            )

            for field in required:
                self.require_non_empty_string(
                    c[field],
                    field
                )

    # =========================
    # RELATION TYPES
    # =========================

    def _validate_relation_types(
        self,
        conocimientos,
        permitidos
    ):

        for c in conocimientos:

            if c["tipo_relacion"] not in permitidos:

                self.result.add(
                    f"Tipo de relación inválido: "
                    f"{c['tipo_relacion']}"
                )

    # =========================
    # DUPLICATES
    # =========================

    def _validate_duplicates(
        self,
        conocimientos
    ):

        seen = set()

        for c in conocimientos:

            key = (
                c["concepto_a"].strip().lower(),
                c["relacion"].strip().lower(),
                c["concepto_b"].strip().lower()
            )

            if key in seen:
                self.result.add(
                    f"Conocimiento duplicado: {key}"
                )

            seen.add(key)

    # =========================
    # EXPLANATIONS
    # =========================

    def _validate_explanations(
        self,
        conocimientos
    ):

        for c in conocimientos:

            if len(
                c["explicacion"].strip()
            ) < 20:

                self.result.add(
                    "Explicación demasiado corta"
                )

    # =========================
    # CONTRADICTIONS
    # =========================

    def _validate_contradictions(
        self,
        conocimientos
    ):

        relations = {}

        for c in conocimientos:

            key = (
                c["concepto_a"].lower(),
                c["relacion"].lower()
            )

            value = c["concepto_b"].lower()

            if key in relations:

                if relations[key] != value:

                    self.result.add(
                        f"Posible contradicción detectada "
                        f"para {c['concepto_a']}"
                    )

            relations[key] = value