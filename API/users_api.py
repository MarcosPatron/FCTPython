from flask import Blueprint, request, jsonify
from data_base.users_repository import UsersRepository
from data_base.tipo_users_repository import TipoUsersRepository
from utils.jwt_handler import generate_jwt

class UserAPI:
    def __init__(self):
        self.blueprint = Blueprint('users', __name__, url_prefix='/api/backend')
        self.register_routes()

    def register_routes(self):
        bp = self.blueprint

        @bp.route('/log_in', methods=['POST'])
        def log_in():
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')  # Asegúrate de validar contraseña si es necesario

            if not username or not password:
                return jsonify({'error': 'Faltan credenciales'}), 400

            try:
                user = UsersRepository.find_by_username(username)
                if user:
                    tipo = TipoUsersRepository.get_all_tipos()
                    tipo_usuario = next(
                        (t['NOMBRE_TIPO'] for t in tipo if t['TIPO_USERS_ID'] == user['TIPO_USERS_ID']), "Desconocido"
                    )
                    token = generate_jwt(username)
                    return jsonify({
                        "fullname": user.get("FULLNAME"),
                        "username": user.get("USERNAME"),
                        "email": user.get("EMAIL"),
                        "JWToken": token,
                        "profilePicture": user.get("PROFILE_PICTURE") or "",
                        "tipoUsuario": tipo_usuario
                    })
                return jsonify({'error': 'Usuario no encontrado'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/sign_in', methods=['POST'])
        def sign_in():
            data = request.get_json()
            fullname = data.get('fullname')
            username = data.get('username')
            email = data.get('email')

            if not all([fullname, username, email]):
                return jsonify({'error': 'Campos obligatorios faltantes'}), 400

            try:
                UsersRepository.create_user(fullname, username, email)
                token = generate_jwt(username)
                return jsonify({
                    "fullname": fullname,
                    "username": username,
                    "email": email,
                    "JWToken": token,
                    "profilePicture": "",
                    "tipoUsuario": "Usuario"
                }), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/users/<int:user_id>', methods=['PUT'])
        def edit_user(user_id):
            data = request.get_json()
            fullname = data.get('fullname')
            username = data.get('username')
            email = data.get('email')

            if not username:
                return jsonify({'error': 'Username obligatorio'}), 400

            try:
                UsersRepository.update_user(fullname, username, email)
                return jsonify({'message': f'Usuario {user_id} actualizado'})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
        def delete_user(user_id):
            try:
                UsersRepository.delete_user(user_id)
                return jsonify({'message': f'Usuario {user_id} eliminado'})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/user_types', methods=['GET'])
        def get_user_types():
            try:
                tipos = TipoUsersRepository.get_all_tipos()
                return jsonify(tipos)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
