from app import app

@app.route("/")
def home():
    return "Welcome to the Recipe Website!"
