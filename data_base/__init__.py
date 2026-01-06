# data_base/__init__.py

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# 🔹 Cargar variables solo si existe .env (para local)
if os.path.exists(".env"):
    load_dotenv()

def get_connection():
    """
    Devuelve una conexión a la base de datos MySQL.
    Detecta automáticamente si está en Railway o en local.
    """
    try:
        # Railway MySQL plugin usa estas variables
        host = os.getenv("MYSQLHOST") or os.getenv("DB_HOST")
        port = int(os.getenv("MYSQLPORT", os.getenv("DB_PORT", 3306)))
        user = os.getenv("MYSQLUSER") or os.getenv("DB_USER")
        password = os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD")
        database = os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME")

        if not all([host, user, password, database]):
            raise ValueError("Faltan variables de entorno de la base de datos")

        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        return conn

    except Error as e:
        # Loguea el error y lanza excepción para evitar 500 sin explicación
        print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
        raise

    except ValueError as ve:
        print(f"[ERROR] {ve}")
        raise

# 🔹 Importar repositorios
from data_base.users_repository import UsersRepository
from data_base.logs_repository import LogsRepository
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository
from data_base.attachments_repository import AttachmentsRepository
from data_base.tickets_repository import TicketsRepository

