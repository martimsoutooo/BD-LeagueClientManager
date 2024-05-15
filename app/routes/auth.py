from flask import Blueprint, request, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..data.models import create_user, get_user_by_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Password = request.form.get('Password')
        
        # Verifica se o usuário já existe
        if get_user_by_username(Name):
            return jsonify({"status": "error", "message": "Name already exists"}), 409

        # Cria um novo usuário
        create_user(Name, Email, generate_password_hash(Password, method='sha256'))
        return jsonify({"status": "success", "message": "Registration successful"})

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Password = request.form.get('Password')

        # Verifica as credenciais do usuário
        user = get_user_by_username(Name)
        if user and check_password_hash(user.Password, Password):
            return jsonify({"status": "success", "message": "Login successful"})
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return render_template('login.html')

