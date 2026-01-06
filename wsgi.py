# wsgi.py
# Punto de entrada para Gunicorn en Railway

from flask import Flask
from dotenv import load_dotenv
import os

# Importa los blueprints
from API.assistants_api import assistants_bp
from API.users_api import UserAPI
from API.tickets_api import TicketAPI


def create_app():
    """
    Crea y configura la aplicación Flask.
    """
    # Cargar .env SOLO en local
    if os.getenv("RAILWAY_ENVIRONMENT") is None and os.path.exists(".env"):
        load_dotenv()

    app = Flask(__name__)

    user_api = UserAPI()
    ticket_api = TicketAPI()

    app.register_blueprint(assistants_bp)
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(ticket_api.blueprint)

    return app


# App global requerida por Gunicorn
app = create_app()


# Este bloque solo sirve para desarrollo local
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
