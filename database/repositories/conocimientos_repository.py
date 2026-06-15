from database.repositories.base_repository import BaseRepository

from models.conocimiento import Conocimiento


class ConocimientosRepository(BaseRepository):

    def _to_model(self, row):
        if not row:
            return None

        return Conocimiento(
            id=row["id"],
            bloque_id=row["bloque_id"],
            temario_id=row["temario_id"],
            concepto_a=row["concepto_a"],
            tipo_relacion=row["tipo_relacion"],
            relacion=row["relacion"],
            concepto_b=row["concepto_b"],
            explicacion=row["explicacion"],
            nivel_dificultad=row["nivel_dificultad"],
            orden_aprendizaje=row["orden_aprendizaje"]
        )

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
        conocimiento_id = self._execute(
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

        return self.get_by_id(conocimiento_id)

    def get_by_id(self, conocimiento_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM conocimientos
            WHERE id = ?
            """,
            (conocimiento_id,)
        )

        return self._to_model(row)

    def get_by_bloque(self, bloque_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM conocimientos
            WHERE bloque_id = ?
            ORDER BY orden_aprendizaje ASC
            """,
            (bloque_id,)
        )

        return [self._to_model(row) for row in rows]

    def get_by_temario(self, temario_id):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM conocimientos
            WHERE temario_id = ?
            ORDER BY orden_aprendizaje ASC
            """,
            (temario_id,)
        )

        return [self._to_model(row) for row in rows]

    def find_duplicate(
        self,
        concepto_a,
        relacion,
        concepto_b
    ):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM conocimientos
            WHERE concepto_a = ?
              AND relacion = ?
              AND concepto_b = ?
            LIMIT 1
            """,
            (
                concepto_a,
                relacion,
                concepto_b
            )
        )

        return self._to_model(row)

    def count_by_bloque(self, bloque_id):
        row = self._fetchone_raw(
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
            """
            DELETE FROM conocimientos
            WHERE id = ?
            """,
            (conocimiento_id,)
        )