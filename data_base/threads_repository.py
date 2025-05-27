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
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_threads_by_user(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM THREADS WHERE USER_ID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
