from data_base import get_connection

class TipoUsersRepository:

    @staticmethod
    def get_all_tipos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM TIPO_USERS"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
