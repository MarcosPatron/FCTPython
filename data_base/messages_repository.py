from data_base import get_connection

class MessagesRepository:

    @staticmethod
    def create_message(thread_id, type_, content, id_message):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO MESSAGES (THREAD_ID, TYPE, CONTENT, ID_MESSAGE)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (thread_id, type_, content, id_message))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_messages_by_thread(thread_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM MESSAGES WHERE THREAD_ID = %s ORDER BY CREATED_AT ASC"
        cursor.execute(query, (thread_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
