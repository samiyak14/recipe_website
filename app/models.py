from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(255))  # Stores relative file path
    video_path = db.Column(db.String(255))  # Stores relative file path
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)