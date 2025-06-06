# data_base/users_repository.py

from data_base import get_connection
from werkzeug.security import generate_password_hash
from data_base.tickets_repository import TicketsRepository  # Necesario para borrar tickets

class UsersRepository:

    @staticmethod
    def find_by_username(username):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM USERS WHERE USERNAME = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create_user(fullname, username, email, password):
        conn = get_connection()
        cursor = conn.cursor()
        hashed_pw = generate_password_hash(password)

        query = """
            INSERT INTO USERS (USERNAME, FULLNAME, EMAIL, PASSWORD)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (username, fullname, email, hashed_pw))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_user(fullname, new_username, email, username_original):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE USERS SET FULLNAME = %s, USERNAME = %s, EMAIL = %s
            WHERE USERNAME = %s
        """
        cursor.execute(query, (fullname, new_username, email, username_original))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_user_by_username(username):
        conn = get_connection()
        cursor = conn.cursor()

        # Obtener el USERSID
        cursor.execute("SELECT USERSID FROM USERS WHERE USERNAME = %s", (username,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            raise ValueError(f"Usuario '{username}' no encontrado")

        user_id = row[0]

        # Eliminar primero sus tickets
        TicketsRepository.delete_tickets_by_user_id(user_id)

        # Luego eliminar el usuario
        cursor.execute("DELETE FROM USERS WHERE USERSID = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
