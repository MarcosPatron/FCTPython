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
    coordinates = data.get('coordinates')

    if not mensaje or not username:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    try:
        # Parsear coordenadas a string
        coordinates_str = ""
        if coordinates:
            if isinstance(coordinates, dict):
                coordinates_str = (
                    f"Latitud: {coordinates.get('lat')}, "
                    f"Longitud: {coordinates.get('lng')}"
                )
            elif isinstance(coordinates, list):
                coordinates_str = ", ".join(map(str, coordinates))
            else:
                coordinates_str = str(coordinates)

        # Mensaje final para el asistente
        mensaje_asistente = mensaje
        if coordinates_str:
            mensaje_asistente += f". Coordenadas del usuario: {coordinates_str}"

        # Buscar el ID del usuario
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
            return jsonify({'error': f'Usuario "{username}" no encontrado'}), 404

        user_id = row[0]
        nuevo_hilo = False

        # Crear o recuperar hilo
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
                return jsonify({'error': f'Hilo "{uuid_thread}" no encontrado'}), 404

        MessagesRepository.create_message(
            thread_id=threadsid,
            type_='user',
            content=mensaje_asistente
        )

        # Ejecutar agente
        result = asyncio.run(
            Runner.run(triage_agent_instance, mensaje_asistente)
        )

        # Respuesta del agente
        output = getattr(result, "final_output", "[Sin contenido]")

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
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500
