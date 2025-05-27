from flask import Flask
from API.assistants_api import assistants_bp
#from API.users_api import users_bp
from dotenv import load_dotenv
import os

def create_app():
    # Cargar variables de entorno desde .env
    load_dotenv()

    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(assistants_bp)
    #app.register_blueprint(users_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
