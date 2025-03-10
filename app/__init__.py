from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from .models import db,Recipe,Admin
from flask_login import LoginManager, current_user

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder="static")

    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))  # Fetch the user by ID
    # Register Blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    login_manager.login_view = 'routes.admin_login'  # Redirect if user is not logged in
    login_manager.login_message_category = "danger"

    

    return app

