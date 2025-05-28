from flask import Flask
from dotenv import load_dotenv
import os

# Importa los blueprints desde la carpeta api (en minúsculas)
from api.assistants_api import assistants_bp
from api.users_api import UserAPI
from api.ticktes_api import TicketAPI  # usa tickets_api si era un error tipográfico


def create_app():
    # Cargar variables de entorno desde .env
    load_dotenv()

    app = Flask(__name__)

    # Instanciar y registrar blueprints personalizados
    user_api = UserAPI()
    ticket_api = TicketAPI()

    app.register_blueprint(assistants_bp)
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(ticket_api.blueprint)

    return app


# Punto de entrada si corres localmente (útil para desarrollo)
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

