from dataclasses import dataclass
from typing import Optional


@dataclass
class Temario:
    id: Optional[int]
    bloque_id: int
    titulo: Optional[str]
    contenido: str
    orden: int = 1