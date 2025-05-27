from data_base import get_connection

class AttachmentsRepository:

    @staticmethod
    def add_attachment(thread_id, filename, content_type, file_content):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO ATTACHMENTS (THREAD_ID, FILENAME, CONTENT_TYPE, FILE_CONTENT)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (thread_id, filename, content_type, file_content))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_attachments_by_thread(thread_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ATTACHMENTSID, FILENAME, CONTENT_TYPE, CREATED_AT FROM ATTACHMENTS WHERE THREAD_ID = %s"
        cursor.execute(query, (thread_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
