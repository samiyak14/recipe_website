from app import db, create_app  # Import your Flask app factory function
from sqlalchemy import text
app = create_app()  # Create Flask app instance

with app.app_context():  # Push the application context
    result = db.session.execute(text("PRAGMA table_info(Recipe)")).fetchall()
    for row in result:
        print(row)