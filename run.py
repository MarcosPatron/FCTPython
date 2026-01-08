from flask import Flask
from dotenv import load_dotenv
import os

# Importa los blueprints desde la carpeta API
from API.assistants_api import assistants_bp
from API.users_api import UserAPI
from API.tickets_api import TicketAPI

def create_app():
    load_dotenv()
    app = Flask(__name__)

    user_api = UserAPI()
    ticket_api = TicketAPI()

    app.register_blueprint(assistants_bp)
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(ticket_api.blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000)) # Puerto de la API
    app.run(host="0.0.0.0", port=port, debug=True)
