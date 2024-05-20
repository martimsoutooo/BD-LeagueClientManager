from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ..data.models import buy_champion, buy_skin, get_user_balance
from ..data.database import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('login.html')

@main_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT Name FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_name = cursor.fetchone()[0]

    return render_template('dashboard.html', user_name=user_name)

@main_bp.route('/game')
def game():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT Rank_Points, RP FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_data = cursor.fetchone()
    user_rank_points = user_data[0]

    return render_template('game.html', user_rank_points=user_rank_points)

@main_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    balance = get_user_balance(user_id)
    user_be = balance.BE
    user_rp = balance.RP
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
    SELECT C.ID, C.Name, C.Category, C.Kingdom 
    FROM LCM.Champion C
    JOIN LCM.User_Item UI ON C.ID = UI.ID_Item
    WHERE UI.ID_User = ?
    """, (user_id,))
    champions = cursor.fetchall()
    
    return render_template('profile.html', user_be=user_be, user_rp=user_rp, champions=champions)

@main_bp.route('/store')
def store():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    balance = get_user_balance(user_id)
    user_be = balance.BE
    user_rp = balance.RP
    
    db = get_db()
    cursor = db.cursor()
    
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    champion_query = """
    SELECT C.ID, C.Name, C.BE_Price, C.Category, C.Kingdom 
    FROM LCM.Champion C
    WHERE C.ID NOT IN (
        SELECT UI.ID_Item 
        FROM LCM.User_Item UI 
        WHERE UI.ID_User = ?
    )
    """
    params = [user_id]
    
    if kingdom != 'all':
        champion_query += " AND C.Kingdom = ?"
        params.append(kingdom)
    if category != 'all':
        champion_query += " AND C.Category = ?"
        params.append(category)
    if alphabetical == '1':
        champion_query += " ORDER BY C.Name"
    else:
        champion_query += " ORDER BY C.ID"

    cursor.execute(champion_query, params)
    champions = cursor.fetchall()
    
    cursor.execute("SELECT LCM.Skin.Name as skin, LCM.Champion.Name as champion, LCM.Skin.RP_Price as rp_price FROM LCM.Skin JOIN LCM.Champion ON LCM.Skin.Champion_ID = LCM.Champion.ID")
    skins = cursor.fetchall()

    return render_template('store.html', champions=champions, skins=skins, user_be=user_be, user_rp=user_rp)

@main_bp.route('/buy_champion_route', methods=['POST'])
def buy_champion_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    print("in")

    data = request.get_json()
    champion_id = data.get('champion_id')
    be_price = data.get('be_price')
    
    result = buy_champion(user_id, int(champion_id), int(be_price))
    print(jsonify(result))
    return jsonify(result)

@main_bp.route('/buy_skin_route', methods=['POST'])
def buy_skin_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    data = request.get_json()
    skin_id = data.get('skin_id')
    rp_price = data.get('rp_price')
    
    result = buy_skin(user_id, skin_id, rp_price)
    return jsonify(result)

@main_bp.route('/filter_champions', methods=['GET'])
def filter_champions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    champion_query = """
    SELECT C.ID, C.Name, C.BE_Price, C.Category, C.Kingdom 
    FROM LCM.Champion C
    WHERE C.ID NOT IN (
        SELECT UI.ID_Item 
        FROM LCM.User_Item UI 
        WHERE UI.ID_User = ?
    )
    """
    params = [user_id]
    
    if kingdom != 'all':
        champion_query += " AND C.Kingdom = ?"
        params.append(kingdom)
    if category != 'all':
        champion_query += " AND C.Category = ?"
        params.append(category)
    if alphabetical == '1':
        champion_query += " ORDER BY C.Name"
    else:
        champion_query += " ORDER BY C.ID"

    cursor.execute(champion_query, params)
    champions = cursor.fetchall()
    
    champions_list = [
        {
            "ID": champ[0],
            "Name": champ[1],
            "BE_Price": champ[2],
            "Category": champ[3],
            "Kingdom": champ[4]
        }
        for champ in champions
    ]
    
    return jsonify({"status": "success", "champions": champions_list})

@main_bp.route('/purchase_rp', methods=['POST'])
def purchase_rp():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    data = request.get_json()
    rp_amount = data.get('rp_amount')
    
    if not rp_amount or int(rp_amount) <= 0:
        return jsonify({"status": "error", "message": "Invalid amount"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("UPDATE LCM.[User] SET RP = RP + ? WHERE ID = ?", (rp_amount, user_id))
    db.commit()
    
    return jsonify({"status": "success", "message": f"{rp_amount} RP added successfully"})
