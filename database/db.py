import sqlite3
import logging

from config.settings import DB_PATH

logger = logging.getLogger(__name__)


def get_connection():
    """
    Devuelve una conexión SQLite configurada para los repositories.
    """
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode=WAL")

    return conn