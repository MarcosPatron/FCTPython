# data_base/__init__.py

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Solo cargar .env en local
if os.getenv("RAILWAY_ENVIRONMENT") is None and os.path.exists(".env"):
    load_dotenv()

def get_connection():
    try:
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
            database=database,
            connection_timeout=5,     # 🔑 CRÍTICO
            autocommit=True          # evita locks tontos
        )

        return conn

    except Exception as e:
        print(f"[DB ERROR] {e}")
        raise
