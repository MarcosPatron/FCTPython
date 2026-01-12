from data_base import get_connection

class DesfibriladoresRepository:

    @staticmethod
    def get_all(limit=50):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT situacion, direccion
            FROM desfibriladores
            ORDER BY situacion
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
