from database.repositories.base_repository import BaseRepository

from models.pregunta import Pregunta


class PreguntasRepository(BaseRepository):

    def _to_model(self, row):
        if not row:
            return None

        return Pregunta(
            id=row["id"],
            conocimiento_id=row["conocimiento_id"],
            tipo=row["tipo"],
            pregunta=row["pregunta"]
        )

    def create(
        self,
        conocimiento_id,
        tipo,
        pregunta
    ):
        pregunta_id = self._execute(
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

        return self.get_by_id(pregunta_id)

    def get_by_id(self, pregunta_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM preguntas
            WHERE id = ?
            """,
            (pregunta_id,)
        )

        return self._to_model(row)

    def get_by_conocimiento(self, conocimiento_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM preguntas
            WHERE conocimiento_id = ?
            """,
            (conocimiento_id,)
        )

        return [self._to_model(row) for row in rows]

    def get_by_bloque(self, bloque_id):
        rows = self._fetchall_raw(
            """
            SELECT p.*
            FROM preguntas p
            JOIN conocimientos c
                ON p.conocimiento_id = c.id
            WHERE c.bloque_id = ?
            """,
            (bloque_id,)
        )

        return [self._to_model(row) for row in rows]

    def count_by_bloque(self, bloque_id):
        row = self._fetchone_raw(
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
            """
            DELETE FROM preguntas
            WHERE id = ?
            """,
            (pregunta_id,)
        )