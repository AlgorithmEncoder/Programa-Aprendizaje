from database.repositories.base_repository import BaseRepository

from models.bloque import Bloque


class BloquesRepository(BaseRepository):

    def _to_model(self, row):
        if not row:
            return None

        return Bloque(
            id=row["id"],
            tema_id=row["tema_id"],
            numero=row["numero"],
            titulo=row["titulo"],
            descripcion=row["descripcion"]
        )

    def create(
        self,
        tema_id,
        numero,
        titulo,
        descripcion=None
    ):
        bloque_id = self._execute(
            """
            INSERT INTO bloques (
                tema_id,
                numero,
                titulo,
                descripcion
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                tema_id,
                numero,
                titulo,
                descripcion
            )
        )

        return self.get_by_id(bloque_id)

    def get_by_id(self, bloque_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM bloques
            WHERE id = ?
            """,
            (bloque_id,)
        )

        return self._to_model(row)

    def get_by_tema(self, tema_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM bloques
            WHERE tema_id = ?
            ORDER BY numero ASC
            """,
            (tema_id,)
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def get_by_tema_and_numero(
        self,
        tema_id,
        numero
    ):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM bloques
            WHERE tema_id = ?
            AND numero = ?
            """,
            (
                tema_id,
                numero
            )
        )

        return self._to_model(row)

    def update(
        self,
        bloque_id,
        numero,
        titulo,
        descripcion
    ):
        self._execute(
            """
            UPDATE bloques
            SET numero = ?,
                titulo = ?,
                descripcion = ?
            WHERE id = ?
            """,
            (
                numero,
                titulo,
                descripcion,
                bloque_id
            )
        )

        return self.get_by_id(bloque_id)

    def delete(self, bloque_id):
        self._execute(
            """
            DELETE FROM bloques
            WHERE id = ?
            """,
            (bloque_id,)
        )