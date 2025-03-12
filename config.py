import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "recipes.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'abcd12349876')  # Change this to a secure key!

    # Upload Folders
    UPLOAD_FOLDER_PROFILE = os.path.join(basedir, 'app/static/uploads/profile_pics')
    UPLOAD_FOLDER_RECIPES = os.path.join(basedir, 'app/static/uploads/recipe_media')

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi','webp'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
