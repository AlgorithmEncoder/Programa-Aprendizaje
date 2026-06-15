from database.repositories.base_repository import BaseRepository


class TemariosRepository(BaseRepository):

    def create(
        self,
        bloque_id,
        titulo,
        contenido,
        orden=1
    ):
        return self._execute(
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

    def get_by_id(self, temario_id):
        return self._fetchone(
            "SELECT * FROM temario WHERE id = ?",
            (temario_id,)
        )

    def get_by_bloque(self, bloque_id):
        return self._fetchall(
            """
            SELECT *
            FROM temario
            WHERE bloque_id = ?
            ORDER BY orden ASC
            """,
            (bloque_id,)
        )

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

    def delete(self, temario_id):
        self._execute(
            "DELETE FROM temario WHERE id = ?",
            (temario_id,)
        )

    def count_by_bloque(self, bloque_id):
        row = self._fetchone(
            """
            SELECT COUNT(*) AS total
            FROM temario
            WHERE bloque_id = ?
            """,
            (bloque_id,)
        )

        return row["total"]