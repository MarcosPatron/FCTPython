from flask import Blueprint, request, jsonify
from data_base.tickets_repository import TicketsRepository

class TicketAPI:
    def __init__(self):
        self.blueprint = Blueprint('tickets', __name__, url_prefix='/api/backend')
        self.register_routes()

    def register_routes(self):
        bp = self.blueprint

        @bp.route('/send_ticket', methods=['POST'])
        def send_ticket():
            data = request.get_json()
            user_id = data.get('user_id')
            subject = data.get('subject')
            message = data.get('message')

            if not all([user_id, subject, message]):
                return jsonify({'error': 'Faltan campos'}), 400

            try:
                success = TicketsRepository.create_ticket(user_id, asunto, descripcion, categoria, prioridad)
                return jsonify(success)
            except Exception as e:
                return jsonify({'error': str(e)}), 500





