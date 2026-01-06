# data_base/__init__.py

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar .env SOLO en local
if os.getenv("RAILWAY_ENVIRONMENT") is None and os.path.exists(".env"):
    load_dotenv()


def get_connection():
    """
    Devuelve una conexión MySQL segura para Railway o local.
    La conexión DEBE cerrarse tras su uso.
    """
    try:
        host = os.getenv("MYSQLHOST") or os.getenv("DB_HOST")
        port = int(os.getenv("MYSQLPORT", os.getenv("DB_PORT", 3306)))
        user = os.getenv("MYSQLUSER") or os.getenv("DB_USER")
        password = os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD")
        database = os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME")

        if not all([host, user, password, database]):
            raise ValueError("Faltan variables de entorno de MySQL")

        return mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connection_timeout=5,   # ⏱ evita bloqueos
            autocommit=True         # 🧠 reduce locks y RAM
        )

    except Error as e:
        print(f"[DB ERROR] Error conectando a MySQL: {e}")
        raise

    except ValueError as ve:
        print(f"[DB CONFIG ERROR] {ve}")
        raise


# 🔹 Importar repositorios (NO crean conexión al importar)
from data_base.users_repository import UsersRepository
from data_base.logs_repository import LogsRepository
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository
from data_base.attachments_repository import AttachmentsRepository
from data_base.tickets_repository import TicketsRepository
