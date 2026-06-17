import os

# ===== MODEL =====
OPENAI_MODEL = "gpt-4.1-mini"
TEMPERATURE_DEFAULT = 0.3
MAX_TOKENS_DEFAULT = 2000
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ===== LÍMITES =====
DEFAULT_NUM_BLOQUES = 10

MIN_TEMARIOS_PER_BLOCK = 7
MAX_TEMARIOS_PER_BLOCK = 10

MIN_CONOCIMIENTOS = 20
MAX_CONOCIMIENTOS = 50

MIN_PREGUNTAS = 20
MAX_PREGUNTAS = 50

RESPUESTAS_INCORRECTAS_POR_PREGUNTA = 3

# ===== PEDAGÓGICOS =====
NIVEL_EDUCATIVO_DEFAULT = "general"  # primaria, secundaria, universitario
PROFUNDIDAD_DEFAULT = "media"
TIPOS_RELACION_PERMITIDOS = [
    "clasificacion",
    "propiedad",
    "funcion",
    "ubicacion",
    "composicion",
    "causa",
    "consecuencia",
    "proceso"
]

# ===== FASES =====
ENABLE_PHASE_1 = True
ENABLE_PHASE_2 = True
ENABLE_PHASE_3 = True
ENABLE_PHASE_4 = True
ENABLE_PHASE_5 = True
ENABLE_PHASE_6 = True

# ===== DATABASE =====
DB_PATH = "database.db"

# ===== LOGGING =====
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
LOG_PATH = "logs/app.log"

LOG_AI_CALLS = True
LOG_TOKENS = True
LOG_COST_ESTIMATION = True

ENABLE_COST_TRACKING = True
COST_PER_1K_INPUT_TOKENS = 0.0005
COST_PER_1K_OUTPUT_TOKENS = 0.0015

ESTADOS_GENERACION = [
    "pendiente",
    "ejecutando",
    "generado",
    "validado",
    "revisando",
    "aprobado",
    "completado",
    "error"
]

# ===== SAFETY =====
MAX_RETRIES_PER_PHASE = 3
STRICT_JSON_MODE = True

# ===== REVIEWS =====
ENABLE_REVIEWS = False

REVIEWS_PER_PHASE = {
    "fase1": 0,
    "fase2": 0,
    "fase3": 0,
    "fase4": 0,
    "fase5": 0,
    "fase6": 0,
}


PHASE_ORDER = [
    "fase1",
    "fase2",
    "fase3",
    "fase4",
    "fase5",
    "fase6"
]