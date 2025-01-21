# app/models.py

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)  # Comma-separated ingredients
    steps = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(200), nullable=True)  # Optional: URL to video
    is_premium = db.Column(db.Boolean, default=False)  # True for premium, False for free

    def get_ingredients_list(self):
        return self.ingredients.split(',')  # Splits the ingredients into a list
