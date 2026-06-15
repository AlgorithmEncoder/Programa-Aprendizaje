import json
from database.db import get_connection
from config.settings import ESTADOS_GENERACION
from database.repositories.base_repository import BaseRepository


class GeneracionesRepository(BaseRepository):
    """
    Servicio para gestión de generaciones IA.
    Sin estado interno.
    """
    
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
        query = """
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
        """

        params = (
            tema_nombre,
            fase,
            estado,
            subfase,
            numero_bloque,
            json.dumps(json_entrada) if json_entrada else None,
            prompt,
            modelo,
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        generacion_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return generacion_id

    # =========================
    # READ
    # =========================
    def get_by_id(self, generacion_id):
        return self._fetchone(
            "SELECT * FROM generaciones WHERE id = ?",
            (generacion_id,)
        )

    def list_recent(self, limit=100):
        query = """
        SELECT * FROM generaciones
        ORDER BY id DESC
        LIMIT ?
        """
        rows = self._execute(query, (limit,), fetchall=True)
        return [dict(r) for r in rows]

    def get_by_phase(self, fase):
        query = """
        SELECT * FROM generaciones
        WHERE fase = ?
        ORDER BY id DESC
        """
        rows = self._execute(query, (fase,), fetchall=True)
        return [dict(r) for r in rows]

    def get_by_topic(self, tema_nombre):
        query = """
        SELECT * FROM generaciones
        WHERE tema_nombre = ?
        ORDER BY id DESC
        """
        rows = self._execute(query, (tema_nombre,), fetchall=True)
        return [dict(r) for r in rows]

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
        query = """
        UPDATE generaciones
        SET estado = 'error',
            json_salida = ?
        WHERE id = ?
        """

        self._execute(
            query,
            (json.dumps({"error": mensaje_error}), generacion_id)
        )

    # =========================
    # RECOVERY HELPERS
    # =========================
    def get_pending(self):
        query = """
        SELECT * FROM generaciones
        WHERE estado = 'pendiente'
        ORDER BY id ASC
        """
        rows = self._execute(query, fetchall=True)
        return [dict(r) for r in rows]

    def get_errors(self):
        query = """
        SELECT * FROM generaciones
        WHERE estado = 'error'
        ORDER BY id DESC
        """
        rows = self._execute(query, fetchall=True)
        return [dict(r) for r in rows]

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

        row = self._execute(query, params, fetchone=True)
        return self._row_to_dict(row)