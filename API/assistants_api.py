from flask import Blueprint, request, jsonify
import uuid
import traceback
import asyncio
from assistant.system_agents import triage_agent_instance
from repositories.threads_repository import ThreadsRepository
from repositories.messages_repository import MessagesRepository
from agents import Runner

assistants_bp = Blueprint('assistants', __name__)
thread_map = {}

@assistants_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    mensaje = data.get('Message')
    uuid_thread = data.get('ThreadId')
    user_id = data.get('UserId')  # Se asume que lo envías en la petición

    if not mensaje:
        return jsonify({'error': 'Falta el mensaje'}), 400
    if not user_id:
        return jsonify({'error': 'Falta el user_id'}), 400

    try:
        nuevo_hilo = False
        if not uuid_thread:
            uuid_thread = str(uuid.uuid4())
            nuevo_hilo = True

        if nuevo_hilo:
            ThreadsRepository.create_thread(
                user_id=user_id,
                provider='triage',
                status='active',
                id_thread=uuid_thread,
                description='Conversación inicial'
            )

        # Guardar mensaje del usuario
        MessagesRepository.create_message(
            thread_id=uuid_thread,
            type_='user',
            content=mensaje,
            id_message=str(uuid.uuid4())
        )

        # Recuperar historial del hilo para dar contexto al asistente
        historial_raw = MessagesRepository.get_messages_by_thread(uuid_thread)

        history = [
            {"role": "user" if m["TYPE"] == "user" else "assistant", "content": m["CONTENT"]}
            for m in historial_raw
        ]

        # Ejecutar agente con contexto
        result = asyncio.run(Runner.run(triage_agent_instance, mensaje, history=history))

        openai_thread_id = thread_map.get(uuid_thread)
        thread_map[uuid_thread] = getattr(result, "thread_id", openai_thread_id)

        output = getattr(result, "final_output", "[Sin contenido]")

        # Guardar respuesta del asistente
        MessagesRepository.create_message(
            thread_id=uuid_thread,
            type_='assistant',
            content=output,
            id_message=str(uuid.uuid4())
        )

        return jsonify({
            'threadId': uuid_thread,
            'message': output,
            'description': "Respuesta generada por el agente Triage"
        })

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
