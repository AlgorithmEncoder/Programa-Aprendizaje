from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ValidationResult:
    """
    Resultado estándar de cualquier validación.
    """
    is_valid: bool
    error: Optional[str] = None
    data: Optional[Any] = None

    @classmethod
    def success(cls, data: Any = None):
        return cls(is_valid=True, error=None, data=data)

    @classmethod
    def fail(cls, error: str):
        return cls(is_valid=False, error=error)