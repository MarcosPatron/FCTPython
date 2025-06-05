from flask import Blueprint, request, jsonify
import uuid
import traceback
import asyncio

from assistant.system_agents import triage_agent_instance
from data_base.threads_repository import ThreadsRepository
from data_base.messages_repository import MessagesRepository
from agents import Runner
from data_base import get_connection

assistants_bp = Blueprint('assistants', __name__)
thread_map = {}

@assistants_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()

    mensaje = data.get('Message')
    uuid_thread = data.get('ThreadId')  # ID_THREAD (UUID externo)
    username = data.get('Username')
    coordinates = data.get('coordinates', [])

    if not mensaje or not username:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    try:
        # Buscar el ID numérico del usuario
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT USERSID FROM USERS WHERE USERNAME = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return jsonify({'error': f'Usuario \"{username}\" no encontrado'}), 404

        user_id = row[0]
        nuevo_hilo = False

        # Si no se recibe UUID externo, generarlo
        if not uuid_thread:
            uuid_thread = str(uuid.uuid4())
            nuevo_hilo = True

        # Crear nuevo hilo o recuperar THREADSID
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
                return jsonify({'error': f'Hilo \"{uuid_thread}\" no encontrado'}), 404

        # Guardar mensaje del usuario
        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='user',
            content=mensaje
        )

        # Ejecutar agente (sin history)
        result = asyncio.run(Runner.run(triage_agent_instance, mensaje))

        # Respuesta del agente
        output = getattr(result, "final_output", "[Sin contenido]")

        # Guardar respuesta del agente
        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='assistant',
            content=output
        )

        return jsonify({
            'threadId': uuid_thread,
            'message': output,
            'description': "Respuesta generada por el agente Triage"
        })

    except Exception as e:
        print("Error en /send_message:", traceback.format_exc())
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
