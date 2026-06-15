from database.repositories.base_repository import BaseRepository


class TemasRepository(BaseRepository):

    def create(self, nombre, descripcion=None):
        return self._execute(
            """
            INSERT INTO temas (nombre, descripcion)
            VALUES (?, ?)
            """,
            (nombre, descripcion)
        )

    def get_by_id(self, tema_id):
        return self._fetchone(
            "SELECT * FROM temas WHERE id = ?",
            (tema_id,)
        )

    def get_by_name(self, nombre):
        return self._fetchone(
            "SELECT * FROM temas WHERE nombre = ?",
            (nombre,)
        )

    def list_all(self):
        return self._fetchall(
            "SELECT * FROM temas ORDER BY nombre"
        )

    def update(self, tema_id, nombre, descripcion):
        self._execute(
            """
            UPDATE temas
            SET nombre = ?, descripcion = ?
            WHERE id = ?
            """,
            (nombre, descripcion, tema_id)
        )

    def delete(self, tema_id):
        self._execute(
            "DELETE FROM temas WHERE id = ?",
            (tema_id,)
        )

    def exists(self, nombre):
        return self.get_by_name(nombre) is not None