from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from ..data.models import create_user, get_user_by_username, verify_user, get_user_by_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Received: username={username}, email={email}, password={password}")  # Debugging
        
        # Verifica se o usuário já existe
        if get_user_by_username(username):
            return jsonify({"status": "error", "message": "Username already exists"}), 409
        if get_user_by_email(email):
            return jsonify({"status": "error", "message": "Email already exists"}), 409

        # Cria um novo usuário
        create_user(username, email, password)
        user = get_user_by_username(username)
        session['user_id'] = user.ID
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verifica as credenciais do usuário
        user = verify_user(username, password)
        if user:
            # Configura a sessão do usuário
            session['user_id'] = user.ID
            print(f"User {user.ID} logged in successfully")
            return redirect(url_for('main.dashboard'))
        else:
            print("Login failed: Invalid credentials")
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))

