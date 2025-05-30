from flask import Blueprint, request, jsonify
from data_base.tickets_repository import TicketsRepository
from data_base.users_repository import UsersRepository  # necesario

class TicketAPI:
    def __init__(self):
        self.blueprint = Blueprint('tickets', __name__, url_prefix='/api/backend')
        self.register_routes()

    def register_routes(self):
        bp = self.blueprint

        @bp.route('/send_ticket', methods=['POST'])
        def send_ticket():
            data = request.get_json()
            print("✅ Datos recibidos del frontend:", data)

            usuario = data.get('usuario')
            categoria = data.get('categoria')
            prioridad = data.get('prioridad')
            descripcion = data.get('descripcion')

            if not all([usuario, categoria, prioridad, descripcion]):
                print("❌ Faltan campos")
                return jsonify({'error': 'Faltan campos'}), 400

            username = usuario.get('username')
            print("🔍 Username recibido:", username)

            if not username:
                return jsonify({'error': 'Falta username'}), 400

            try:
                user = UsersRepository.find_by_username(username)
                if not user:
                    print("❌ Usuario no encontrado en BBDD")
                    return jsonify({'error': 'Usuario no encontrado'}), 404

                user_id = user['USERSID']
                print("🆔 ID del usuario:", user_id)

                success = TicketsRepository.create_ticket(
                    user_id=user_id,
                    categoria=categoria,
                    prioridad=prioridad,
                    descripcion=descripcion
                )
                print("🎫 Ticket creado con éxito")
                return jsonify({'success': success})
            except Exception as e:
                import traceback
                print("💥 Excepción al crear ticket:")
                traceback.print_exc()
                return jsonify({'error': str(e)}), 500
