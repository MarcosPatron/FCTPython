# data_base/tickets_repository.py

from data_base import get_connection

class TicketsRepository:

    @staticmethod
    def create_ticket(user_id, descripcion, categoria, prioridad):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO TICKETS_SOPORTE (USER_ID, DESCRIPCION, CATEGORIA, PRIORIDAD)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, descripcion, categoria, prioridad))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_tickets_by_user(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM TICKETS_SOPORTE WHERE USER_ID = %s ORDER BY CREADO_EN DESC"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def update_ticket_status(ticket_id, nuevo_estado):
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE TICKETS_SOPORTE SET ESTADO = %s WHERE TICKET_ID = %s"
        cursor.execute(query, (nuevo_estado, ticket_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_tickets_by_user_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM TICKETS_SOPORTE WHERE USER_ID = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
