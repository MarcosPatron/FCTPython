from data_base import get_connection
from werkzeug.security import generate_password_hash

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
        query = "DELETE FROM USERS WHERE USERNAME = %s"
        cursor.execute(query, (username,))
        conn.commit()
        cursor.close()
        conn.close()

