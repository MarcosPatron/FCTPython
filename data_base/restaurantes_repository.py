from data_base import get_connection

class RestaurantesRepository:

    @staticmethod
    def get_all(limit=50):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT nombre, direccion, telefono, web
            FROM restaurantes
            ORDER BY nombre
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
