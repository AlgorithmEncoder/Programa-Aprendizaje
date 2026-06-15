from database.repositories.base_repository import BaseRepository


class ConocimientosRepository(BaseRepository):

    def create(
        self,
        bloque_id,
        temario_id,
        concepto_a,
        tipo_relacion,
        relacion,
        concepto_b,
        explicacion,
        nivel_dificultad=1,
        orden_aprendizaje=1
    ):
        return self._execute(
            """
            INSERT INTO conocimientos (
                bloque_id,
                temario_id,
                concepto_a,
                tipo_relacion,
                relacion,
                concepto_b,
                explicacion,
                nivel_dificultad,
                orden_aprendizaje
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                bloque_id,
                temario_id,
                concepto_a,
                tipo_relacion,
                relacion,
                concepto_b,
                explicacion,
                nivel_dificultad,
                orden_aprendizaje
            )
        )

    def get_by_id(self, conocimiento_id):
        return self._fetchone(
            "SELECT * FROM conocimientos WHERE id = ?",
            (conocimiento_id,)
        )

    def get_by_bloque(self, bloque_id):
        return self._fetchall(
            """
            SELECT *
            FROM conocimientos
            WHERE bloque_id = ?
            ORDER BY orden_aprendizaje
            """,
            (bloque_id,)
        )

    def get_by_temario(self, temario_id):
        return self._fetchall(
            """
            SELECT *
            FROM conocimientos
            WHERE temario_id = ?
            ORDER BY orden_aprendizaje
            """,
            (temario_id,)
        )

    def find_duplicate(
        self,
        concepto_a,
        relacion,
        concepto_b
    ):
        return self._fetchone(
            """
            SELECT *
            FROM conocimientos
            WHERE concepto_a = ?
            AND relacion = ?
            AND concepto_b = ?
            """,
            (
                concepto_a,
                relacion,
                concepto_b
            )
        )

    def count_by_bloque(self, bloque_id):
        row = self._fetchone(
            """
            SELECT COUNT(*) AS total
            FROM conocimientos
            WHERE bloque_id = ?
            """,
            (bloque_id,)
        )

        return row["total"]

    def delete(self, conocimiento_id):
        self._execute(
            "DELETE FROM conocimientos WHERE id = ?",
            (conocimiento_id,)
        )