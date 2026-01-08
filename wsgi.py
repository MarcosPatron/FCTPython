from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Importa tus blueprints
from API.assistants_api import assistants_bp
from API.users_api import UserAPI
from API.tickets_api import TicketAPI

def create_app():
    if os.getenv("RAILWAY_ENVIRONMENT") is None:
        load_dotenv()

    app = Flask(__name__)

    # Registrar blueprints
    user_api = UserAPI()
    # ticket_api = TicketAPI()  # si lo tienes
    app.register_blueprint(assistants_bp)
    app.register_blueprint(user_api.blueprint)
    # app.register_blueprint(ticket_api.blueprint)

    # 🔹 Endpoint de prueba rápido
    @app.route("/ping")
    def ping():
        return jsonify({"status": "ok"}), 200

    return app

# App global
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
