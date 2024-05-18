from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
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
    
    db = get_db()
    cursor = db.cursor()
    
    # Fetch user's Blue Essence and Riot Points
    cursor.execute("SELECT BE, RP FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_data = cursor.fetchone()
    user_be = user_data[0]
    user_rp = user_data[1]
    
    # Fetch champions owned by the user
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
    
    db = get_db()
    cursor = db.cursor()
    
    # Get filter values from request
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    # Build the query with filters
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
        champion_query += " ORDER BY C.ID"  # Assuming this is the original order

    # Execute the query with filters
    cursor.execute(champion_query, params)
    champions = cursor.fetchall()
    
    # Fetch skins data
    cursor.execute("SELECT LCM.Skin.Name as skin, LCM.Champion.Name as champion, LCM.Skin.RP_Price as rp_price FROM LCM.Skin JOIN LCM.Champion ON LCM.Skin.Champion_ID = LCM.Champion.ID")
    skins = cursor.fetchall()

    # Fetch user's balance
    cursor.execute("SELECT BE,RP FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_data = cursor.fetchone()
    user_be = user_data[0]
    user_rp = user_data[1]
    
    return render_template('store.html', champions=champions, skins=skins, user_be=user_be, user_rp=user_rp)

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
        
        # Adicionar campeão à tabela User_Item
        cursor.execute("INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora) VALUES (?, ?, GETDATE(), GETDATE())", (user_id, champion_id))
        
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
        champion_query += " ORDER BY C.ID"  # Assuming this is the original order

    # Execute the query with filters
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
    
    # Atualiza o saldo de RP do usuário
    cursor.execute("UPDATE LCM.[User] SET RP = RP + ? WHERE ID = ?", (rp_amount, user_id))
    db.commit()
    
    return jsonify({"status": "success", "message": f"{rp_amount} RP added successfully"})

@main_bp.route('/buy_skin', methods=['POST'])
def buy_skin():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    data = request.get_json()
    skin_id = data.get('skin_id')
    rp_price = data.get('rp_price')
    
    print(f"Received skin_id: {skin_id}, rp_price: {rp_price}")  # Log para depuração
    
    if not skin_id or not rp_price:
        return jsonify({"status": "error", "message": "Invalid skin ID or RP price"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT RP FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_rp = cursor.fetchone()[0]
    
    if user_rp >= int(rp_price):
        cursor.execute("UPDATE LCM.[User] SET RP = RP - ? WHERE ID = ?", (rp_price, user_id))
        cursor.execute("INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora) VALUES (?, ?, GETDATE(), GETDATE())", (user_id, skin_id))
        db.commit()
        return jsonify({"status": "success", "message": "Skin purchased successfully"})
    else:
        return jsonify({"status": "error", "message": "Not enough Riot Points"}), 400





