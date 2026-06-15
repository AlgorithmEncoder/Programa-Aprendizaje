from database.repositories.base_repository import BaseRepository


class BloquesRepository(BaseRepository):

    def create(
        self,
        tema_id,
        numero,
        titulo,
        descripcion=None
    ):
        return self._execute(
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

    def get_by_id(self, bloque_id):
        return self._fetchone(
            "SELECT * FROM bloques WHERE id = ?",
            (bloque_id,)
        )

    def get_by_tema(self, tema_id):
        return self._fetchall(
            """
            SELECT *
            FROM bloques
            WHERE tema_id = ?
            ORDER BY numero ASC
            """,
            (tema_id,)
        )

    def get_by_tema_and_numero(
        self,
        tema_id,
        numero
    ):
        return self._fetchone(
            """
            SELECT *
            FROM bloques
            WHERE tema_id = ?
            AND numero = ?
            """,
            (tema_id, numero)
        )

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

    def delete(self, bloque_id):
        self._execute(
            "DELETE FROM bloques WHERE id = ?",
            (bloque_id,)
        )