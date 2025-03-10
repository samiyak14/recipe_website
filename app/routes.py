from flask import Blueprint, render_template,request, redirect, url_for, session, flash
from .models import db, Recipe,Admin
from werkzeug.security import check_password_hash
from functools import wraps
from flask_login import logout_user

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
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('routes.admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
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
    return render_template('admin_dashboard.html')

@bp.route('/admin/add_recipe', methods=['GET', 'POST'])
@admin_required  # Ensure only logged-in admins can access
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        is_premium = 'is_premium' in request.form  # Checkbox for premium recipes

        new_recipe = Recipe(title=title, ingredients=ingredients, steps=steps, is_premium=is_premium)

        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('routes.admin_dashboard'))  # Redirect to admin dashboard

    return render_template('add_recipe.html')



@bp.route('/admin/logout')
@admin_required
def admin_logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.admin_login'))  # Redirect to admin login page
