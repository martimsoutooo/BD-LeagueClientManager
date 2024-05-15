from flask import Flask
from .routes.auth import auth_bp
from .routes.main import main_bp
from .data.database import init_db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configurações do arquivo config.py

    # Inicializa o banco de dados
    init_db(app)

    # Registra os blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

