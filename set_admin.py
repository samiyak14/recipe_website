from app.models import User
from app import db,create_app

app = create_app()

with app.app_context():
    admin = User.query.filter_by(username="samiya").first()  # Find user 
    if admin:
        admin.is_admin = True
        db.session.commit()