from app import create_app, db
from app.models import Recipe  # Ensure this matches your model name

app = create_app()

with app.app_context():
    recipes = Recipe.query.all()  # Corrected variable name
    if recipes:
        print("List of stored recipes:")
        for recipe in recipes:  # Changed variable name to match model
            print(f"Title: {recipe.title}, Image Path: {recipe.image_path},instructions:{recipe.instructions}")
    else:
        print("No recipes found.")
