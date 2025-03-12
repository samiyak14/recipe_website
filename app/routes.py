from flask import Blueprint, render_template,request, redirect, url_for, session, flash,current_app
from .models import db, Recipe,Admin,User
from app.forms import EditProfileForm,SignupForm
from werkzeug.security import check_password_hash
from functools import wraps
from flask_login import logout_user
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required,current_user
import os
from config import Config


bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    recipes = Recipe.query.filter_by(is_premium=False).all()  # Fetch free recipes
    return render_template('index.html', recipes=recipes)


@bp.route('/recipes')
def recipes():
    recipes = Recipe.query.filter_by(is_premium=False).all()  # Fetch non-premium recipes
    return render_template('recipes.html', recipes=recipes)

@bp.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Get recipe or show 404 error
    return render_template('view_recipe.html', recipe=recipe)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')


@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):  # Secure password check
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('routes.admin_dashboard'))
        else:
            flash('Invalid credentials!', 'danger')

    return render_template('admin_login.html')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('You must log in first', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    recipes = Recipe.query.all()  # Fetch all recipes
    return render_template('admin_dashboard.html', recipes=recipes)

@bp.route('/admin/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        tags = request.form.get('tags')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        image_path = None
        video_path = None

        # Handle Image Upload
        image = request.files.get('image')
        if image and Config.allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER_RECIPES'], filename)
            image.save(image_path)
            image_path = f"uploads/recipe_media/{filename}"  # Store relative path

        # Handle Video Upload
        video = request.files.get('video')
        if video and Config.allowed_file(video.filename):
            filename = secure_filename(video.filename)
            video_path = os.path.join(current_app.config['UPLOAD_FOLDER_RECIPES'], filename)
            video.save(video_path)
            video_path = f"uploads/recipe_media/{filename}"

        # Save recipe to database
        new_recipe = Recipe(
            title=title, 
            tags=tags, 
            ingredients=ingredients, 
            instructions=instructions,
            image_path=image_path,
            video_path=video_path
        )

        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe added successfully!', 'success')
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('add_recipe.html')
@bp.route('/admin/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        recipe.tags = request.form.get('tags', '')

        # Handle Image Upload
        image = request.files.get('image')
        if image and Config.allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER_RECIPES'], filename)
            image.save(image_path)
            recipe.image_path = f"uploads/recipe_media/{filename}"  # Update only if a new file is uploaded

        # Handle Video Upload
        video = request.files.get('video')
        if video and Config.allowed_file(video.filename):
            filename = secure_filename(video.filename)
            video_path = os.path.join(current_app.config['UPLOAD_FOLDER_RECIPES'], filename)
            video.save(video_path)
            recipe.video_path = f"uploads/recipe_media/{filename}"  # Update only if a new file is uploaded

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('edit_recipe.html', recipe=recipe)


@bp.route('/admin/delete_recipe/<int:recipe_id>', methods=['POST'])
@admin_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'danger')
    return redirect(url_for('routes.admin_dashboard'))

@bp.route("/admin/logout")
@login_required  # Ensure only logged-in users can access
def admin_logout():
    logout_user()  # Logs out the current user
    flash("You have been logged out.", "success")
    return redirect(url_for("routes.admin_login"))  # Redirect to login page

@bp.route("/user_signup", methods=["GET", "POST"])
def user_signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Default Profile Picture
        profile_photo_filename = "default.jpg"

        # Handle Profile Photo Upload
        if form.profile_photo.data and Config.allowed_file(form.profile_photo.data.filename):
            filename = secure_filename(form.profile_photo.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PROFILE'], filename)
            form.profile_photo.data.save(filepath)
            profile_photo_filename = f"uploads/profile_pics/{filename}"  # Store relative path

        # Create new user
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            profile_photo=profile_photo_filename
        )
        new_user.set_password(form.password.data)  # Hash password before storing
        
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('routes.user_login'))
    
    return render_template('user_signup.html', form=form)

# User Login
@bp.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("routes.user_dashboard"))
        else:
            flash("Invalid email or password!", "danger")

    return render_template("user_login.html")

# User Dashboard
@bp.route("/dashboard")
@login_required  # Only accessible if logged in
def user_dashboard():
    return render_template("user_dashboard.html")

# User Logout
@bp.route("/logout")
@login_required
def user_logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("routes.user_login"))


@bp.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Handle Profile Photo Upload
        if form.profile_photo.data and Config.allowed_file(form.profile_photo.data.filename):
            filename = secure_filename(form.profile_photo.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PROFILE'], filename)
            form.profile_photo.data.save(filepath)
            current_user.profile_photo = f"uploads/profile_pics/{filename}"  # Store relative path

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('routes.user_profile'))

    return render_template('user_profile.html', form=form)
