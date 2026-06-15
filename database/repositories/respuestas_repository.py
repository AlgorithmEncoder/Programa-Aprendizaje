from database.repositories.base_repository import BaseRepository


class RespuestasRepository(BaseRepository):

    def create(
        self,
        pregunta_id,
        texto,
        correcta
    ):
        return self._execute(
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

    def get_by_pregunta(
        self,
        pregunta_id
    ):
        return self._fetchall(
            """
            SELECT *
            FROM respuestas
            WHERE pregunta_id = ?
            """,
            (pregunta_id,)
        )

    def get_correct_answer(
        self,
        pregunta_id
    ):
        return self._fetchone(
            """
            SELECT *
            FROM respuestas
            WHERE pregunta_id = ?
            AND correcta = 1
            LIMIT 1
            """,
            (pregunta_id,)
        )

    def get_incorrect_answers(
        self,
        pregunta_id
    ):
        return self._fetchall(
            """
            SELECT *
            FROM respuestas
            WHERE pregunta_id = ?
            AND correcta = 0
            """,
            (pregunta_id,)
        )

    def delete(self, respuesta_id):
        self._execute(
            "DELETE FROM respuestas WHERE id = ?",
            (respuesta_id,)
        )