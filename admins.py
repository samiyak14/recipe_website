from app import create_app, db
from app.models import Admin  # Ensure this matches your model name

app = create_app()

with app.app_context():
    recipes = Admin.query.all()  # Corrected variable name
    if recipes:
        print("Admins:")
        for recipe in recipes:  # Changed variable name to match model
            print(f"ID={recipe.id}, Username={recipe.username}")
    else:
        print("No Admins found.")
