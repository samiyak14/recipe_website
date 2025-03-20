import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from .models import db, Recipe, Admin, User
from flask_login import LoginManager

migrate = Migrate()
login_manager = LoginManager()

def ensure_upload_folders(app):
    """Ensure the required upload folders exist."""
    os.makedirs(app.config['UPLOAD_FOLDER_PROFILE'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_RECIPES'], exist_ok=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    ensure_upload_folders(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) or Admin.query.get(int(user_id))

    # Register Blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    login_manager.login_view = 'routes.admin_login'  # Redirect if user is not logged in
    login_manager.login_message_category = "danger"

    return app
