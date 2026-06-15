import json
from config.settings import ESTADOS_GENERACION
from database.repositories.base_repository import BaseRepository

from models.generacion import Generacion


class GeneracionesRepository(BaseRepository):
    """
    Servicio para gestión de generaciones IA.
    Sin estado interno.
    """
    
    def _to_model(self, row):
        if not row:
            return None

        return Generacion(
            id=row["id"],
            tema_nombre=row["tema_nombre"],
            fase=row["fase"],
            subfase=row["subfase"],
            numero_bloque=row["numero_bloque"],
            estado=row["estado"],
            json_entrada=row["json_entrada"],
            json_salida=row["json_salida"],
            prompt=row["prompt"],
            modelo=row["modelo"],
            tokens_entrada=row["tokens_entrada"],
            tokens_salida=row["tokens_salida"],
            coste_estimado=row["coste_estimado"]
        )
    
    # =========================
    # CREATE
    # =========================
    def create(
        self,
        tema_nombre,
        fase,
        estado="pendiente",
        subfase=None,
        numero_bloque=None,
        json_entrada=None,
        prompt=None,
        modelo=None,
    ):
        generacion_id = self._execute(
            """
            INSERT INTO generaciones (
                tema_nombre,
                fase,
                estado,
                subfase,
                numero_bloque,
                json_entrada,
                prompt,
                modelo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tema_nombre,
                fase,
                estado,
                subfase,
                numero_bloque,
                json.dumps(json_entrada) if json_entrada else None,
                prompt,
                modelo
            )
        )

        return self.get_by_id(generacion_id)

    # =========================
    # READ
    # =========================
    def get_by_id(self, generacion_id):
        row = self._fetchone_raw(
            """
            SELECT *
            FROM generaciones
            WHERE id = ?
            """,
            (generacion_id,)
        )

        return self._to_model(row)

    def list_recent(self, limit=100):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM generaciones
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def get_by_phase(self, fase):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM generaciones
            WHERE fase = ?
            ORDER BY id DESC
            """,
            (fase,)
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def get_by_topic(self, tema_nombre):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM generaciones
            WHERE tema_nombre = ?
            ORDER BY id DESC
            """,
            (tema_nombre,)
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    # =========================
    # UPDATE ESTADO
    # =========================
    def update_estado(self, generacion_id, estado):
        if estado not in ESTADOS_GENERACION:
            raise ValueError(f"Estado inválido: {estado}")

        query = """
        UPDATE generaciones
        SET estado = ?
        WHERE id = ?
        """
        self._execute(query, (estado, generacion_id))

    # =========================
    # OUTPUT
    # =========================
    def save_output(self, generacion_id, json_salida):
        query = """
        UPDATE generaciones
        SET json_salida = ?
        WHERE id = ?
        """

        self._execute(
            query,
            (json.dumps(json_salida), generacion_id)
        )

    # =========================
    # USAGE / COST
    # =========================
    def save_usage(self, generacion_id, tokens_entrada, tokens_salida, coste_estimado):
        query = """
        UPDATE generaciones
        SET tokens_entrada = ?,
            tokens_salida = ?,
            coste_estimado = ?
        WHERE id = ?
        """

        self._execute(
            query,
            (tokens_entrada, tokens_salida, coste_estimado, generacion_id)
        )

    # =========================
    # PROMPT DEBUG
    # =========================
    def save_prompt(self, generacion_id, prompt):
        query = """
        UPDATE generaciones
        SET prompt = ?
        WHERE id = ?
        """

        self._execute(query, (prompt, generacion_id))

    # =========================
    # ERROR HANDLING
    # =========================
    def mark_error(self, generacion_id, mensaje_error):

        self._execute(
            """
            UPDATE generaciones
            SET estado = ?,
                json_salida = ?
            WHERE id = ?
            """,
            (
                "error",
                json.dumps({
                    "error": mensaje_error
                }),
                generacion_id
            )
        )

    # =========================
    # RECOVERY HELPERS
    # =========================
    def get_pending(self):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM generaciones
            WHERE estado = 'pendiente'
            ORDER BY id ASC
            """
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def get_errors(self):
        rows = self._fetchall_raw(
            """
            SELECT *
            FROM generaciones
            WHERE estado = 'error'
            ORDER BY id DESC
            """
        )

        return [
            self._to_model(row)
            for row in rows
        ]

    def get_last_phase_execution(self, tema_nombre, fase, numero_bloque=None):
        if numero_bloque is not None:
            query = """
            SELECT * FROM generaciones
            WHERE tema_nombre = ?
                AND fase = ?
                AND numero_bloque = ?
            ORDER BY id DESC
            LIMIT 1
            """
            params = (tema_nombre, fase, numero_bloque)
        else:
            query = """
            SELECT * FROM generaciones
            WHERE tema_nombre = ?
                AND fase = ?
            ORDER BY id DESC
            LIMIT 1
            """
            params = (tema_nombre, fase)

        row = self._fetchone_raw(query, params)
        return self._to_model(row)