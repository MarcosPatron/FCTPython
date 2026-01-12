from data_base import get_connection

class ParadasBusRepository:

    @staticmethod
    def get_all(limit=50):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT direccion, lineas, tiempopaso
            FROM paradas_bus
            ORDER BY direccion
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
