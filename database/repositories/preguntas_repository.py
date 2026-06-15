from database.repositories.base_repository import BaseRepository


class PreguntasRepository(BaseRepository):

    def create(
        self,
        conocimiento_id,
        tipo,
        pregunta
    ):
        return self._execute(
            """
            INSERT INTO preguntas (
                conocimiento_id,
                tipo,
                pregunta
            )
            VALUES (?, ?, ?)
            """,
            (
                conocimiento_id,
                tipo,
                pregunta
            )
        )

    def get_by_id(self, pregunta_id):
        return self._fetchone(
            "SELECT * FROM preguntas WHERE id = ?",
            (pregunta_id,)
        )

    def get_by_conocimiento(
        self,
        conocimiento_id
    ):
        return self._fetchall(
            """
            SELECT *
            FROM preguntas
            WHERE conocimiento_id = ?
            """,
            (conocimiento_id,)
        )

    def get_by_bloque(self, bloque_id):
        return self._fetchall(
            """
            SELECT p.*
            FROM preguntas p
            JOIN conocimientos c
                ON p.conocimiento_id = c.id
            WHERE c.bloque_id = ?
            """,
            (bloque_id,)
        )

    def count_by_bloque(self, bloque_id):
        row = self._fetchone(
            """
            SELECT COUNT(*) AS total
            FROM preguntas p
            JOIN conocimientos c
                ON p.conocimiento_id = c.id
            WHERE c.bloque_id = ?
            """,
            (bloque_id,)
        )

        return row["total"]

    def delete(self, pregunta_id):
        self._execute(
            "DELETE FROM preguntas WHERE id = ?",
            (pregunta_id,)
        )