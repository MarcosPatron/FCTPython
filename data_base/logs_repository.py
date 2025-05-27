from data_base import get_connection

class LogsRepository:

    @staticmethod
    def log(mensaje, descripcion, tipo_log, objeto, metodo):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO LOGS (MENSAJE, DESCRIPCION, TIPO_LOG, OBJETO, METODO)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (mensaje, descripcion, tipo_log, objeto, metodo))
        conn.commit()
        cursor.close()
        conn.close()
