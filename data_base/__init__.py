import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables del entorno desde .env
load_dotenv()

# Función central para obtener una conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "fct_database")
    )

from data_base.users_repository import UsersRepository
from data_base.tipo_users_repository import TipoUsersRepository
from data_base.logs_repository import LogsRepository
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository
from data_base.attachments_repository import AttachmentsRepository
from data_base.tickets_repository import TicketsRepository
