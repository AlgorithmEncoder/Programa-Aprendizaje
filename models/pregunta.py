from dataclasses import dataclass
from typing import Optional


@dataclass
class Pregunta:
    id: Optional[int]
    conocimiento_id: int
    tipo: str
    pregunta: str