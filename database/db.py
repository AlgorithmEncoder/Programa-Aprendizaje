import sqlite3
import logging

from config.settings import DB_PATH

logger = logging.getLogger(__name__)


def get_connection():
    """
    Devuelve una conexión SQLite con claves foráneas activadas.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn