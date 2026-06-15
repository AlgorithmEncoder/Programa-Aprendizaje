from database.repositories.base_repository import BaseRepository

from models.respuesta import Respuesta


class RespuestasRepository(BaseRepository):

    def _to_model(self, row):
        if not row:
            return None

        return Respuesta(
            id=row["id"],
            pregunta_id=row["pregunta_id"],
            texto=row["texto"],
            correcta=bool(row["correcta"])
        )

    def create(
        self,
        pregunta_id,
        texto,
        correcta
    ):
        respuesta_id = self._execute(
            """
            INSERT INTO respuestas (
                pregunta_id,
                texto,
                correcta
            )
            VALUES (?, ?, ?)
            """,
            (
                pregunta_id,
                texto,
                int(correcta)
            )
        )

        row = self._fetchone_raw(
            """
            SELECT *
            FROM respuestas
            WHERE id = ?
            """,
            (respuesta_id,)
        )

        return self._to_model(row)

    def get_by_pregunta(self, pregunta_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM respuestas
            WHERE pregunta_id = ?
            """,
            (pregunta_id,)
        )

        return [self._to_model(row) for row in rows]

    def get_correct_answer(self, pregunta_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM respuestas
            WHERE pregunta_id = ?
              AND correcta = 1
            LIMIT 1
            """,
            (pregunta_id,)
        )

        return self._to_model(row)

    def get_incorrect_answers(self, pregunta_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM respuestas
            WHERE pregunta_id = ?
              AND correcta = 0
            """,
            (pregunta_id,)
        )

        return [self._to_model(row) for row in rows]

    def delete(self, respuesta_id):
        self._execute(
            """
            DELETE FROM respuestas
            WHERE id = ?
            """,
            (respuesta_id,)
        )