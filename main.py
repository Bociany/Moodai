from flask import Flask
from api import api
from interface import interface
import secrets

# Create a new flask app
flask_app = Flask(__name__)

# Generate a random secrets key
flask_app.secret_key = secrets.token_bytes(32)

# Register the blueprints for the app
flask_app.register_blueprint(api)
flask_app.register_blueprint(interface)
