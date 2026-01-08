# wsgi.py - Versión definitiva para Railway

from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import asyncio
import traceback

# Importar blueprints y clases
from API.assistants_api import assistants_bp
from API.users_api import UserAPI
from API.tickets_api import TicketAPI

def create_app():
    # 🔹 Cargar .env SOLO en local
    if os.getenv("RAILWAY_ENVIRONMENT") is None and os.path.exists(".env"):
        load_dotenv()

    app = Flask(__name__)

    # 🔹 Registrar blueprints
    user_api = UserAPI()
    ticket_api = TicketAPI()

    app.register_blueprint(assistants_bp)
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(ticket_api.blueprint)

    # 🔹 Endpoint de prueba para Railway /health check
    @app.route("/ping")
    def ping():
        return jsonify({"status": "ok"}), 200

    # 🔹 Manejo de errores globales opcional
    @app.errorhandler(Exception)
    def handle_exception(e):
        print("❌ Excepción global:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    return app

# 🔹 App global requerida por Gunicorn
app = create_app()

# 🔹 Solo para desarrollo local con python wsgi.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
