from pathlib import Path

from config.settings import DB_PATH
from db import get_connection


def create_database():
    """
    Crea todas las tablas necesarias si no existen.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # TEMAS
    # =========================
    cursor.execute("""
    CREATE TABLE temas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # BLOQUES
    # =========================
    cursor.execute("""
    CREATE TABLE bloques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tema_id INTEGER NOT NULL,
        numero INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        FOREIGN KEY (tema_id) REFERENCES temas(id) ON DELETE CASCADE
    )
    """)

    # =========================
    # TEMARIO
    # =========================
    cursor.execute("""
    CREATE TABLE temario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bloque_id INTEGER NOT NULL,
        titulo TEXT,
        contenido TEXT NOT NULL,
        orden INTEGER DEFAULT 1,
        FOREIGN KEY (bloque_id) REFERENCES bloques(id) ON DELETE CASCADE
    )
    """)

    # =========================
    # CONOCIMIENTOS
    # =========================
    cursor.execute("""
    CREATE TABLE conocimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        bloque_id INTEGER NOT NULL,
        temario_id INTEGER,

        concepto_a TEXT NOT NULL,
        tipo_relacion TEXT,
        relacion TEXT NOT NULL,
        concepto_b TEXT NOT NULL,

        explicacion TEXT,

        nivel_dificultad INTEGER DEFAULT 1,
        orden_aprendizaje INTEGER DEFAULT 1,

        FOREIGN KEY (bloque_id) REFERENCES bloques(id) ON DELETE CASCADE,
        FOREIGN KEY (temario_id) REFERENCES temario(id) ON DELETE SET NULL
    )
    """)

    # =========================
    # PREGUNTAS
    # =========================
    cursor.execute("""
    CREATE TABLE preguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        conocimiento_id INTEGER NOT NULL,

        tipo TEXT DEFAULT 'multiple_choice',
        pregunta TEXT NOT NULL,

        FOREIGN KEY (conocimiento_id)
        REFERENCES conocimientos(id)
        ON DELETE CASCADE
    )
    """)

    # =========================
    # RESPUESTAS
    # =========================
    cursor.execute("""
    CREATE TABLE respuestas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        pregunta_id INTEGER NOT NULL,

        texto TEXT NOT NULL,
        correcta INTEGER NOT NULL CHECK(correcta IN (0,1)),

        FOREIGN KEY (pregunta_id)
        REFERENCES preguntas(id)
        ON DELETE CASCADE
    )
    """)

    # =========================
    # GENERACIONES
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tema_nombre TEXT NOT NULL,

        fase TEXT NOT NULL,
        subfase TEXT,

        numero_bloque INTEGER,

        estado TEXT NOT NULL CHECK(
            estado IN (
                'pendiente',
                'ejecutando',
                'completado',
                'error',
                'validado'
            )
        )

        json_entrada TEXT,
        json_salida TEXT,

        prompt TEXT,
        modelo TEXT,

        tokens_entrada INTEGER DEFAULT 0,
        tokens_salida INTEGER DEFAULT 0,
        coste_estimado REAL DEFAULT 0,

        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    print("Base de datos creada/verificada correctamente.")


def database_is_complete():
    """
    Comprueba que todas las tablas principales existen.
    """

    required_tables = {
        "temas",
        "bloques",
        "temario",
        "conocimientos",
        "preguntas",
        "respuestas",
        "generaciones",
    }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)

    existing_tables = {row[0] for row in cursor.fetchall()}

    conn.close()

    missing = required_tables - existing_tables

    if missing:
        print(f"Faltan tablas: {missing}")
        return False

    return True


def validate_schema():
    """
    Valida que la estructura de la base de datos es correcta.
    """

    expected_schema = {
        "temas": {
            "id",
            "nombre",
            "descripcion",
            "fecha_creacion"
        },
        "bloques": {
            "id",
            "tema_id",
            "numero",
            "titulo",
            "descripcion"
        },
        "temario": {
            "id",
            "bloque_id",
            "titulo",
            "contenido",
            "orden"
        },
        "conocimientos": {
            "id",
            "bloque_id",
            "temario_id",
            "concepto_a",
            "tipo_relacion",
            "relacion",
            "concepto_b",
            "explicacion",
            "nivel_dificultad",
            "orden_aprendizaje"
        },
        "preguntas": {
            "id",
            "conocimiento_id",
            "tipo",
            "pregunta"
        },
        "respuestas": {
            "id",
            "pregunta_id",
            "texto",
            "correcta"
        },
        "generaciones": {
            "id",
            "tema_nombre",
            "fase",
            "subfase",
            "numero_bloque",
            "estado",
            "json_entrada",
            "json_salida",
            "prompt",
            "modelo",
            "tokens_entrada",
            "tokens_salida",
            "coste_estimado",
            "fecha_creacion"
        }
    }

    conn = get_connection()
    cursor = conn.cursor()

    errors = []

    for table, expected_columns in expected_schema.items():

        cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
        """, (table,))

        if not cursor.fetchone():
            errors.append(f"❌ Falta la tabla: {table}")
            continue

        cursor.execute(f"PRAGMA table_info({table})")
        real_columns = {row[1] for row in cursor.fetchall()}

        missing_cols = expected_columns - real_columns
        extra_cols = real_columns - expected_columns

        if missing_cols:
            errors.append(f"❌ {table} → faltan columnas: {missing_cols}")

        if extra_cols:
            errors.append(f"⚠️ {table} → columnas extra: {extra_cols}")

    conn.close()

    if errors:
        print("\nERRORES DE ESQUEMA DETECTADOS:")
        for error in errors:
            print(error)
        return False

    print("Esquema de base de datos correcto.")
    return True


def initialize_database():
    """
    Inicializa y valida la base de datos.
    """

    if not Path(DB_PATH).exists():
        print("Base de datos no encontrada.")
        create_database()

    elif not validate_schema():
        print("Recreando base de datos...")
        create_database()

    if validate_schema():
        print("Base de datos lista para usar.")
    else:
        print("La base de datos tiene problemas.")


if __name__ == "__main__":
    initialize_database()