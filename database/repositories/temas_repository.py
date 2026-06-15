from database.repositories.base_repository import BaseRepository

from models.tema import Tema


class TemasRepository(BaseRepository):

    def _to_model(self, row):
        if not row:
            return None

        return Tema(
            id=row["id"],
            nombre=row["nombre"],
            descripcion=row["descripcion"]
        )

    def create(self, nombre, descripcion=None):
        tema_id = self._execute(
            """
            INSERT INTO temas (
                nombre,
                descripcion
            )
            VALUES (?, ?)
            """,
            (
                nombre,
                descripcion
            )
        )

        return self.get_by_id(tema_id)

    def get_by_id(self, tema_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM temas
            WHERE id = ?
            """,
            (tema_id,)
        )

        return self._to_model(row)

    def get_by_name(self, nombre):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM temas
            WHERE nombre = ?
            """,
            (nombre,)
        )

        return self._to_model(row)

    def list_all(self):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM temas
            ORDER BY nombre ASC
            """
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def update(
        self,
        tema_id,
        nombre,
        descripcion
    ):
        self._execute(
            """
            UPDATE temas
            SET nombre = ?,
                descripcion = ?
            WHERE id = ?
            """,
            (
                nombre,
                descripcion,
                tema_id
            )
        )

        return self.get_by_id(tema_id)

    def delete(self, tema_id):
        self._execute(
            """
            DELETE FROM temas
            WHERE id = ?
            """,
            (tema_id,)
        )

    def exists(self, nombre):
        return self.get_by_name(nombre) is not None