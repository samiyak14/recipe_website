from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

db = SQLAlchemy()

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

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
    likes = db.relationship('Like', backref='recipe', lazy=True)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)
    comments = db.relationship('Comment', backref='recipe', lazy=True) 

    @property
    def average_rating(self):
        """Calculate the average rating for the recipe."""
        if not self.ratings:
            return 0  # No ratings yet
        return round(sum(r.rating for r in self.ratings) / len(self.ratings), 1)

    @property
    def like_count(self):
        """Get total number of likes for the recipe."""
        return len(self.likes)


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
    is_admin=db.Column(db.Boolean, default=False)
    liked_recipes = db.relationship('Recipe', secondary='like', backref='liked_by')

    def set_password(self, password):
        """Hashes and sets the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the password is correct."""
        return check_password_hash(self.password_hash, password)
    

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating from 1 to 5

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='comments', lazy=True)

 
