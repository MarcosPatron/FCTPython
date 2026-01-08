from flask import Blueprint, request, jsonify
import uuid
import traceback
import asyncio
import time
import logging

from assistant.system_agents import triage_agent_instance
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository
from agents import Runner
from data_base import get_connection

# ---- CONFIGURACIÓN DE LOGGING ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

assistants_bp = Blueprint('assistants', __name__)

@assistants_bp.route('/send_message', methods=['POST'])
def send_message():
    start_time = time.time()
    logging.info("1️⃣ /send_message — request recibido")

    try:
        data = request.get_json(force=True, silent=True)
        logging.info("2️⃣ JSON recibido: %s", data)

        if not data:
            logging.warning("JSON vacío o inválido")
            return jsonify({'error': 'JSON vacío o inválido'}), 400

        # Acepta mayúsculas y minúsculas (producción + Android)
        mensaje = data.get('Message') or data.get('message')
        uuid_thread = data.get('ThreadId') or data.get('threadId')
        username = data.get('Username') or data.get('username')
        coordinates = data.get('coordinates', [])

        if not mensaje or not username:
            logging.warning("Faltan datos obligatorios: mensaje=%s, username=%s", mensaje, username)
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        logging.info("3️⃣ Datos validados")

        # ---- DB: usuario ----
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT USERSID FROM USERS WHERE USERNAME = %s",
            (username,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            logging.warning("Usuario '%s' no encontrado", username)
            return jsonify({'error': f'Usuario \"{username}\" no encontrado'}), 404

        user_id = row[0]
        nuevo_hilo = False

        if not uuid_thread:
            uuid_thread = str(uuid.uuid4())
            nuevo_hilo = True

        if nuevo_hilo:
            threadsid = ThreadsRepository.create_thread(
                user_id=user_id,
                provider='triage',
                status='active',
                id_thread=uuid_thread,
                description='Conversación inicial'
            )
        else:
            threadsid = ThreadsRepository.get_threadsid_by_uuid(uuid_thread)
            if not threadsid:
                logging.warning("Hilo '%s' no encontrado", uuid_thread)
                return jsonify({'error': f'Hilo \"{uuid_thread}\" no encontrado'}), 404

        logging.info("4️⃣ Thread OK: %s", uuid_thread)

        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='user',
            content=mensaje
        )

        logging.info("5️⃣ Mensaje usuario guardado")

        # ---- EJECUCIÓN DEL AGENTE (PUNTO CRÍTICO) ----
        logging.info("6️⃣ Antes de ejecutar Runner.run()")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            Runner.run(triage_agent_instance, mensaje)
        )

        loop.close()

        logging.info("7️⃣ Después de ejecutar Runner.run()")

        output = getattr(result, "final_output", "[Sin contenido]")

        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='assistant',
            content=output
        )

        elapsed = round(time.time() - start_time, 2)
        logging.info("8️⃣ Respuesta enviada (%ss)", elapsed)

        return jsonify({
            'threadId': uuid_thread,
            'message': output,
            'description': "Respuesta generada por el agente Triage",
            'elapsed_seconds': elapsed
        })

    except Exception as e:
        logging.error("❌ ERROR EN /send_message")
        logging.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500
