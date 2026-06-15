from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Generacion:
    id: Optional[int]

    tema_nombre: str
    fase: str
    subfase: Optional[str]
    numero_bloque: Optional[int]

    estado: str

    json_entrada: Any | None = None
    json_salida: Any | None = None

    prompt: Optional[str] = None
    modelo: Optional[str] = None

    tokens_entrada: int = 0
    tokens_salida: int = 0
    coste_estimado: float = 0.0