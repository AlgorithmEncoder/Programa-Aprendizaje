from dataclasses import dataclass
from typing import Optional


@dataclass
class Respuesta:
    id: Optional[int]
    pregunta_id: int
    texto: str
    correcta: bool