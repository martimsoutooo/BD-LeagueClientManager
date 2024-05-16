from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/game')
def game():
    return render_template('game.html')

@main_bp.route('/profile')
def profile():
    return render_template('profile.html')

@main_bp.route('/store')
def store():
    return render_template('store.html')