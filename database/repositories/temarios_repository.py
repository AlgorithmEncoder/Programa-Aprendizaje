from database.repositories.base_repository import BaseRepository

from models.temario import Temario


class TemariosRepository(BaseRepository):

    def _to_model(self, row):
        if not row:
            return None

        return Temario(
            id=row["id"],
            bloque_id=row["bloque_id"],
            titulo=row["titulo"],
            contenido=row["contenido"],
            orden=row["orden"]
        )

    def create(
        self,
        bloque_id,
        titulo,
        contenido,
        orden=1
    ):
        temario_id = self._execute(
            """
            INSERT INTO temario (
                bloque_id,
                titulo,
                contenido,
                orden
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                bloque_id,
                titulo,
                contenido,
                orden
            )
        )

        return self.get_by_id(temario_id)

    def get_by_id(self, temario_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM temario
            WHERE id = ?
            """,
            (temario_id,)
        )

        return self._to_model(row)

    def get_by_bloque(self, bloque_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM temario
            WHERE bloque_id = ?
            ORDER BY orden ASC
            """,
            (bloque_id,)
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def update(
        self,
        temario_id,
        titulo,
        contenido,
        orden
    ):
        self._execute(
            """
            UPDATE temario
            SET titulo = ?,
                contenido = ?,
                orden = ?
            WHERE id = ?
            """,
            (
                titulo,
                contenido,
                orden,
                temario_id
            )
        )

        return self.get_by_id(temario_id)

    def delete(self, temario_id):
        self._execute(
            """
            DELETE FROM temario
            WHERE id = ?
            """,
            (temario_id,)
        )

    def count_by_bloque(self, bloque_id):
        row = self._fetchone_raw(
            """
            SELECT COUNT(*) AS total
            FROM temario
            WHERE bloque_id = ?
            """,
            (bloque_id,)
        )

        return row["total"]