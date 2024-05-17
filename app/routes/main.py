from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ..data.database import get_db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('login.html')

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
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()
    
    # Get filter values from request
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    # Build the query with filters
    champion_query = "SELECT ID_Item_Type, Name, BE_Price, Category, Kingdom FROM LCM.Champion WHERE 1=1"
    params = []
    if kingdom != 'all':
        champion_query += " AND Kingdom = ?"
        params.append(kingdom)
    if category != 'all':
        champion_query += " AND Category = ?"
        params.append(category)
    if alphabetical == '1':
        champion_query += " ORDER BY Name"
    else:
        champion_query += " ORDER BY ID_Item_Type"  # Assuming this is the original order

    # Execute the query with filters
    cursor.execute(champion_query, params)
    champions = cursor.fetchall()
    
    # Fetch skins data
    cursor.execute("SELECT LCM.Skin.Name as skin, LCM.Champion.Name as champion, LCM.Skin.RP_Price as rp_price FROM LCM.Skin JOIN LCM.Champion ON LCM.Skin.Champion_ID = LCM.Champion.ID_Item_Type")
    skins = cursor.fetchall()

    # Fetch user's balance
    cursor.execute("SELECT BE FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_be = cursor.fetchone()[0]
    
    return render_template('store.html', champions=champions, skins=skins, user_be=user_be)
@main_bp.route('/buy_champion', methods=['POST'])
def buy_champion():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    data = request.get_json()
    champion_id = data.get('champion_id')
    be_price = data.get('be_price')
    
    db = get_db()
    cursor = db.cursor()
    
    # Verificar se o usuário possui BE suficiente
    cursor.execute("SELECT BE FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_be = cursor.fetchone()[0]
    
    if user_be >= int(be_price):
        # Deduzir o preço do BE do usuário
        cursor.execute("UPDATE LCM.[User] SET BE = BE - ? WHERE ID = ?", (be_price, user_id))
        
        # Obter a data e a hora atuais
        current_time = datetime.now()
        current_date = current_time.date()
        current_hour = current_time.time()
        
        print(f"Inserting into User_Item: user_id={user_id}, champion_id={champion_id}, date={current_date}, time={current_hour}")
        
        # Adicionar campeão à tabela User_Item com data e hora atuais
        cursor.execute("""
            INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora) 
            VALUES (?, ?, ?, ?)
        """, (user_id, champion_id, current_date, current_hour))
        
        db.commit()
        return jsonify({"status": "success", "message": "Champion purchased successfully"})
    else:
        return jsonify({"status": "error", "message": "Not enough Blue Essence"}), 400

@main_bp.route('/filter_champions', methods=['GET'])
def filter_champions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # Get filter values from request
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    # Build the query with filters
    champion_query = "SELECT ID_Item_Type, Name, BE_Price, Category, Kingdom FROM LCM.Champion WHERE 1=1"
    params = []
    if kingdom != 'all':
        champion_query += " AND Kingdom = ?"
        params.append(kingdom)
    if category != 'all':
        champion_query += " AND Category = ?"
        params.append(category)
    if alphabetical == '1':
        champion_query += " ORDER BY Name"
    else:
        champion_query += " ORDER BY ID_Item_Type"  # Assuming this is the original order

    # Execute the query with filters
    cursor.execute(champion_query, params)
    champions = cursor.fetchall()
    
    champions_list = [
        {
            "ID_Item_Type": champ[0],
            "Name": champ[1],
            "BE_Price": champ[2],
            "Category": champ[3],
            "Kingdom": champ[4]
        }
        for champ in champions
    ]
    
    return jsonify({"status": "success", "champions": champions_list})


