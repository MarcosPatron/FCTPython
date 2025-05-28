# api/__init__.py

from .user_api import UserAPI
from .ticket_api import TicketAPI
from .assistants_api import assistants_bp


def register_blueprints(app):
    # Instanciar clases con blueprints
    user_api = UserAPI()
    ticket_api = TicketAPI()

    # Registrar todos los blueprints en la aplicación
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(ticket_api.blueprint)
    app.register_blueprint(assistants_bp)

