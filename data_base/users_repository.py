from data_base import get_connection

class UsersRepository:

    @staticmethod
    def find_by_username_and_email(username, email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM USERS WHERE USERNAME = %s AND EMAIL = %s"
        cursor.execute(query, (username, email))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def create_user(fullname, username, email):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO USERS (TIPO_USERS_ID, USERNAME, FULLNAME, EMAIL)
            VALUES (%s, %s, %s, %s)
        """
        # Por defecto asignamos tipo de usuario 1
        cursor.execute(query, (1, username, fullname, email))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_user(fullname, username, email):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE USERS SET FULLNAME = %s, EMAIL = %s
            WHERE USERNAME = %s
        """
        cursor.execute(query, (fullname, email, username))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM USERS WHERE USERSID = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
