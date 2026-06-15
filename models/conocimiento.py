from dataclasses import dataclass
from typing import Optional


@dataclass
class Conocimiento:
    id: Optional[int]

    bloque_id: int
    temario_id: Optional[int]

    concepto_a: str
    tipo_relacion: Optional[str]
    relacion: str
    concepto_b: str

    explicacion: Optional[str]

    nivel_dificultad: int = 1
    orden_aprendizaje: int = 1