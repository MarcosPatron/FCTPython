from flask import Flask
from API.assistants_api import assistants_bp
# from API.users_api import users_bp
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.register_blueprint(assistants_bp)
    # app.register_blueprint(users_bp)
    return app

# Este bloque solo corre cuando ejecutas directamente `python run.py`
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

# Este bloque corre siempre, y lo usará Gunicorn
app = create_app()
