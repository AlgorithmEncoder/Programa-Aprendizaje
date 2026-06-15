from dataclasses import dataclass
from typing import Optional


@dataclass
class Bloque:
    id: Optional[int]
    tema_id: int
    numero: int
    titulo: str
    descripcion: Optional[str] = None