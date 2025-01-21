# app/routes.py

from flask import Blueprint, render_template
from .models import Recipe,db  # Import Recipe model

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    recipes = Recipe.query.filter_by(is_premium=False).all()  # Fetch non-premium recipes
    return render_template('index.html', recipes=recipes)

@bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    # Placeholder for future admin functionality
    return render_template('admin.html')
@bp.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)
