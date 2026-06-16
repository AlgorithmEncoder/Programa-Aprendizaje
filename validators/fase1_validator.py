from validators.base_validator import (
    BaseValidator,
    ValidationError
)


class Fase1Validator(BaseValidator):

    def validate(self, output_json):
        
        self.result = self.new_result()

        self._validate_root(output_json)

        conceptos = output_json["conceptos"]

        self._validate_conceptos(conceptos)
        self._validate_unique_names(conceptos)
        self._validate_dependencies_exist(conceptos)
        self._validate_no_cycles(conceptos)

        return True

    # =========================
    # ROOT
    # =========================

    def _validate_root(self, data):

        self.require_keys(
            data,
            ["conceptos"]
        )

        self.require_non_empty_list(
            data["conceptos"],
            "conceptos"
        )

    # =========================
    # CONCEPTOS
    # =========================

    def _validate_conceptos(self, conceptos):

        required = [
            "nombre",
            "descripcion",
            "nivel",
            "depende_de"
        ]

        for concepto in conceptos:

            self.require_keys(
                concepto,
                required
            )

            self.require_non_empty_string(
                concepto["nombre"],
                "nombre"
            )

            self.require_non_empty_string(
                concepto["descripcion"],
                "descripcion"
            )

            if not isinstance(
                concepto["nivel"],
                int
            ):
                self.result.add(
                    "nivel debe ser entero"
                )

            if concepto["nivel"] < 1:
                self.result.add(
                    "nivel inválido"
                )

    def _validate_unique_names(self, conceptos):

        nombres = [
            c["nombre"]
            for c in conceptos
        ]

        self.validate_no_duplicates(
            nombres,
            "nombres conceptos"
        )

    def _validate_dependencies_exist(
        self,
        conceptos
    ):
        nombres = {
            c["nombre"]
            for c in conceptos
        }

        for concepto in conceptos:

            for dep in concepto["depende_de"]:

                if dep not in nombres:
                    self.result.add(
                        f"Dependencia inexistente: {dep}"
                    )

    def _validate_no_cycles(
        self,
        conceptos
    ):
        graph = {
            c["nombre"]: c["depende_de"]
            for c in conceptos
        }

        visited = set()
        stack = set()

        def visit(node):

            if node in stack:
                self.result.add(
                    "Dependencia circular detectada"
                )

            if node in visited:
                return

            stack.add(node)

            for dep in graph[node]:
                visit(dep)

            stack.remove(node)
            visited.add(node)

        for node in graph:
            visit(node)