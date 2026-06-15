from database.db import get_connection


class BaseRepository:

    def _fetchone(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None

    def _fetchall(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    def _execute(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)

        conn.commit()

        lastrowid = cursor.lastrowid

        conn.close()

        return lastrowid