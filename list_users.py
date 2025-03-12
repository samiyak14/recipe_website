from app import create_app, db
from app.models import User  # Assuming your user model is named 'User'

app = create_app()

with app.app_context():
    users = User.query.all()
    if users:
        print("List of registered users:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
    else:
        print("No users found.")
