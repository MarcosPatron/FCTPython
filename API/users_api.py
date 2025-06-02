from flask import Blueprint, request, jsonify
from data_base.users_repository import UsersRepository
from utils.jwt_handler import generate_jwt
from werkzeug.security import check_password_hash

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
            password = data.get('password')

            if not username or not password:
                return jsonify({'error': 'Faltan credenciales'}), 400

            try:
                user = UsersRepository.find_by_username(username)
                if user and check_password_hash(user['PASSWORD'], password):
                    token = generate_jwt(username)
                    return jsonify({
                        "fullname": user.get("FULLNAME"),
                        "username": user.get("USERNAME"),
                        "email": user.get("EMAIL"),
                        "JWToken": token,
                        "profilePicture": user.get("PROFILE_PICTURE") or ""
                    })
                return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/sign_in', methods=['POST'])
        def sign_in():
            data = request.get_json()
            fullname = data.get('fullname')
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not all([fullname, username, email, password]):
                return jsonify({'error': 'Campos obligatorios faltantes'}), 400

            try:
                UsersRepository.create_user(fullname, username, email, password)
                token = generate_jwt(username)
                return jsonify({
                    "fullname": fullname,
                    "username": username,
                    "email": email,
                    "JWToken": token,
                    "profilePicture": ""
                }), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/edit_user/<string:username>', methods=['PUT'])
        def edit_user(username):
            data = request.get_json()
            fullname = data.get('fullname')
            email = data.get('email')
            new_username = data.get('username')  # nuevo username
            password = data.get('password')

            if not username or not password:
                return jsonify({'error': 'Username y contraseña son obligatorios'}), 400

            try:
                user = UsersRepository.find_by_username(username)
                if not user:
                    return jsonify({'error': 'Usuario no encontrado'}), 404

                if not check_password_hash(user['PASSWORD'], password):
                    return jsonify({'error': 'Contraseña incorrecta'}), 401

                # ⚠️ Usamos el username original para buscar y editar
                UsersRepository.update_user(fullname, new_username, email, username)  # <- modificamos el método

                user_actualizado = UsersRepository.find_by_username(new_username)
                token = generate_jwt(new_username)

                return jsonify({
                    "fullname": user_actualizado.get("FULLNAME"),
                    "username": user_actualizado.get("USERNAME"),
                    "email": user_actualizado.get("EMAIL"),
                    "JWToken": token,
                    "profilePicture": user_actualizado.get("PROFILE_PICTURE") or ""
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @bp.route('/delete_user/<string:username>', methods=['DELETE'])
        def delete_user(username):
            try:
                UsersRepository.delete_user_by_username(username)
                return jsonify({'message': f'Usuario {username} eliminado'})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
