from data_base import get_connection

class ThreadsRepository:

    @staticmethod
    def create_thread(user_id, provider, status, id_thread, description):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO THREADS (USER_ID, PROVIDER, STATUS, ID_THREAD, DESCRIPTION)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, provider, status, id_thread, description))
        thread_id_db = cursor.lastrowid  # ← este es el THREADSID (entero)
        conn.commit()
        cursor.close()
        conn.close()
        return thread_id_db  # devolver THREADSID

    @staticmethod
    def get_threadsid_by_uuid(id_thread):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT THREADSID FROM THREADS WHERE ID_THREAD = %s", (id_thread,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else None
