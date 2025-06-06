# api/__init__.py

from .users_api import UserAPI
from .tickets_api import TicketAPI
from .assistants_api import assistants_bp


def register_blueprints(app):
    # Instanciar clases con blueprints
    users_api = UserAPI()
    tickets_api = TicketAPI()

    # Registrar Blueprints en la aplicacion
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(tickets_api.blueprint)
    app.register_blueprint(assistants_bp)

