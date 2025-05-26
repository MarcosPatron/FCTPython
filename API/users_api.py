from flask import Blueprint, request, jsonify
from data_base import db_connection  # asegúrate de tener esta función implementada

users_bp = Blueprint('users', __name__)

# POST /api/backend/logIn
@users_bp.route('log_in', methods=['POST'])
def log_in():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'error': 'Faltan credenciales'}), 400

    try:
        cnx = db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = %s AND EMAIL = %s", (username, email))
        user = cursor.fetchone()

        if user:
            return jsonify(user)
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# POST /api/backend/signIn
@users_bp.route('sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    fullname = data.get('fullname')
    username = data.get('username')
    email = data.get('email')

    if not all([fullname, username, email]):
        return jsonify({'error': 'Campos obligatorios faltantes'}), 400

    try:
        cnx = db_connection()
        cursor = cnx.cursor()
        cursor.execute("""
            INSERT INTO USERS (TIPO_USERS_ID, USERNAME, FULLNAME, EMAIL)
            VALUES (%s, %s, %s, %s)
        """, (1, username, fullname, email))  # TIPO_USERS_ID por defecto 1
        cnx.commit()
        return jsonify({'message': 'Usuario registrado'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# PUT /api/backend/editUser
@users_bp.route('edit_user', methods=['PUT'])
def edit_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    fullname = data.get('fullname')

    if not username:
        return jsonify({'error': 'Username obligatorio'}), 400

    try:
        cnx = db_connection()
        cursor = cnx.cursor()
        cursor.execute("""
            UPDATE USERS SET FULLNAME = %s, EMAIL = %s WHERE USERNAME = %s
        """, (fullname, email, username))
        cnx.commit()
        return jsonify({'message': 'Usuario actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE /api/backend/deleteUser?id=123
@users_bp.route('delete_user', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('id')

    if not user_id:
        return jsonify({'error': 'Falta el ID'}), 400

    try:
        cnx = db_connection()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM USERS WHERE USERSID = %s", (user_id,))
        cnx.commit()
        return jsonify({'message': 'Usuario eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
