import pytest
from flask import Flask
from werkzeug.security import generate_password_hash
from API import UserAPI
from data_base.users_repository import UsersRepository

#  ARREGLOS

@pytest.fixture
def client():
    app = Flask(__name__)
    user_api = UserAPI()
    app.register_blueprint(user_api.blueprint)
    with app.test_client() as client:
        yield client

@pytest.fixture
def user_data():
    return {
        "fullname": "Usuario de Prueba",
        "username": "usuario_test",
        "email": "test@example.com",
        "password": "contrasena123"
    }

# TESTS

def test_sign_in(client, user_data):
    UsersRepository.delete_user_by_username(user_data["username"])

    response = client.post("/api/backend/sign_in", json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == user_data["username"]
    assert "JWToken" in data

def test_log_in(client, user_data):
    UsersRepository.delete_user_by_username(user_data["username"])

    # Crear usuario con hash de contraseña
    hashed = generate_password_hash(user_data["password"])
    UsersRepository.create_user(user_data["fullname"], user_data["username"], user_data["email"], hashed)

    # Hacer login
    response = client.post("/api/backend/log_in", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == user_data["username"]
    assert "JWToken" in data

def test_edit_user(client, user_data):
    new_email = "newemail@example.com"
    new_username = "testuser_updated"

    response = client.put(f"/api/backend/edit_user/{user_data['username']}", json={
        "fullname": user_data["fullname"],
        "username": new_username,
        "email": new_email,
        "password": user_data["password"]
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == new_username
    assert data["email"] == new_email

def test_delete_user(client):
    response = client.delete("/api/backend/delete_user/testuser_updated")
    assert response.status_code == 200
    data = response.get_json()
    assert "eliminado" in data["message"]
