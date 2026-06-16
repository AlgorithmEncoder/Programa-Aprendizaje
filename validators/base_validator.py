from validators.validation_result import ValidationResult


class ValidationError(Exception):
    pass


class BaseValidator:

    def require_keys(self, obj, required_keys):
        for key in required_keys:
            if key not in obj:
                self.result.add(
                    f"Falta clave obligatoria: {key}"
                )

    def require_non_empty_string(self, value, field):
        if not isinstance(value, str) or not value.strip():
            self.result.add(
                f"Campo vacío: {field}"
            )

    def require_non_empty_list(self, value, field):
        if not isinstance(value, list) or len(value) == 0:
            self.result.add(
                f"Lista vacía: {field}"
            )

    def validate_no_duplicates(self, values, field):
        if len(values) != len(set(values)):
            self.result.add(
                f"Duplicados detectados en {field}"
            )
    
    def new_result(self):
        return ValidationResult()

    def raise_if_invalid(self, result: ValidationResult):
        if not result.valid:
            self.result.add("\n".join(result.errors))