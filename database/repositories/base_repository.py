from database.db import get_connection


class BaseRepository:

    def _fetchone_raw(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        row = cursor.fetchone()

        conn.close()

        return row

    def _fetchall_raw(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        rows = cursor.fetchall()

        conn.close()

        return rows

    def _execute(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        lastrowid = cursor.lastrowid

        conn.close()

        return lastrowid