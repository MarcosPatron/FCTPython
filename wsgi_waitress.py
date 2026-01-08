from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Cargar .env solo en local
if os.getenv("RAILWAY_ENVIRONMENT") is None and os.path.exists(".env"):
    load_dotenv()

# Crear app
app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"}), 200

# Registrar tus blueprints aquí si quieres probarlos
# from API.assistants_api import assistants_bp
# app.register_blueprint(assistants_bp)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
