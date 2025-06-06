# api/assistants.py

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
    uuid_thread = data.get('ThreadId')
    username = data.get('Username')
    coordinates = data.get('coordinates', [])

    if not mensaje or not username:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    try:
        # Busca el ID del usuario
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

        # Si no hay UUID(nueva conversacion), lo genera
        if not uuid_thread:
            uuid_thread = str(uuid.uuid4())
            nuevo_hilo = True

        # Crear nuevo hilo o recuperar conversacion
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

        # Añadir coordenadas
        if coordinates:
            mensaje_completo = f"{mensaje}\n(Coordenadas: {coordinates[0]}, {coordinates[1]})"
        else:
            mensaje_completo = mensaje

        # Guardar mensaje en BBDD
        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='user',
            content=mensaje_completo
        )

        result = asyncio.run(Runner.run(triage_agent_instance, mensaje))
        output = getattr(result, "final_output", "[Sin contenido]")

        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='assistant',
            content=output
        )
        # Respuesta API
        return jsonify({
            'threadId': uuid_thread,
            'message': output,
            'description': "Chat del asistente"
        })

    except Exception as e:
        print("Error en /send_message:", traceback.format_exc())
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
