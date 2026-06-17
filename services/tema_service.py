from typing import Optional, Protocol
from models.tema import Tema


class TemasRepositoryProtocol(Protocol):
    def get_by_name(self, nombre: str): ...
    def exists(self, nombre: str) -> bool: ...
    def create(self, *, nombre: str, descripcion: str | None = None): ...
    def list_all(self): ...


class TemasRepository:
    """
    Implementación concreta (ORM / SQL / lo que uses debajo).
    """

    def get_by_name(self, nombre: str):
        return (
            self.session.query(Tema)
            .filter(Tema.nombre == nombre)
            .first()
        )

    def exists(self, nombre: str) -> bool:
        return (
            self.session.query(Tema.id)
            .filter(Tema.nombre == nombre)
            .first()
            is not None
        )

    def create(self, *, nombre: str, descripcion: str | None = None):
        tema = Tema(
            nombre=nombre,
            descripcion=descripcion,
        )
        self.session.add(tema)
        self.session.commit()
        self.session.refresh(tema)
        return tema

    def list_all(self):
        return self.session.query(Tema).all()