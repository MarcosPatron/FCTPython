# data_base/__init__.py

import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables del entorno desde .env
load_dotenv()

# Función central para obtener una conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 3306),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

from data_base.users_repository import UsersRepository
from data_base.tipo_users_repository import TipoUsersRepository
from data_base.logs_repository import LogsRepository
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository
from data_base.attachments_repository import AttachmentsRepository
from data_base.tickets_repository import TicketsRepository
