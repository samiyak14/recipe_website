from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255))
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    image_path = db.Column(db.String(255))  # Stores relative path
    video_path = db.Column(db.String(255))  # Stores relative path
    is_premium = db.Column(db.Boolean, default=False)  # New column


class Admin(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password

    def set_password(self, password):
        """Hashes the password before storing"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password hash"""
        return check_password_hash(self.password_hash, password)
    
class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))  
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_photo = db.Column(db.String(255))  # Store image path
    password_hash = db.Column(db.String(255), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)  # For premium users

    def set_password(self, password):
        """Hashes and sets the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the password is correct."""
        return check_password_hash(self.password_hash, password)