# assistants_api.py

from flask import Blueprint, request, jsonify
import uuid
import traceback
import asyncio
from assistant.system_agents import triage_agent_instance  # <-- el agente creado una sola vez

assistants_bp = Blueprint('assistants', __name__)
thread_map = {}

@assistants_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    mensaje = data.get('Message')
    uuid_thread = data.get('ThreadId')

    if not mensaje:
        return jsonify({'error': 'Falta el mensaje'}), 400

    try:
        if not uuid_thread:
            uuid_thread = str(uuid.uuid4())

        openai_thread_id = thread_map.get(uuid_thread)
        from agents import Runner
        result = asyncio.run(Runner.run(triage_agent_instance, mensaje))

        thread_map[uuid_thread] = getattr(result, "thread_id", openai_thread_id)
        output = getattr(result, "final_output", "[Sin contenido]")

        return jsonify({
            'threadId': uuid_thread,
            'message': output,
            'description': "Respuesta generada por el agente Triage"
        })

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
