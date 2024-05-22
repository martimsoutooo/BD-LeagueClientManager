from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ..data.models import buy_champion, buy_skin, get_user_balance, buy_ward, buy_chest,purchaseRP
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

    # Fetching user rank points and RP
    cursor.execute("SELECT Rank_Points, RP FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_data = cursor.fetchone()
    user_rank_points, user_rp = user_data

    # Fetching champions owned by the user
    cursor.execute("""
    SELECT C.ID, C.Name, C.Category, C.Kingdom 
    FROM LCM.Champion C
    JOIN LCM.User_Item UI ON C.ID = UI.ID_Item
    WHERE UI.ID_User = ?
    """, (user_id,))
    champions = cursor.fetchall()

    # Fetching skins owned by the user
    cursor.execute("""
    SELECT S.ID, S.Name AS skin, C.Name AS championName
    FROM LCM.Skin S
    JOIN LCM.Champion C ON S.Champion_ID = C.ID
    JOIN LCM.User_Item UI ON S.ID = UI.ID_Item
    WHERE UI.ID_User = ?
    """, (user_id,))
    skins = cursor.fetchall()

    # Fetching wards owned by the user
    cursor.execute("""
    SELECT W.ID, W.Name AS ward
    FROM LCM.Ward W
    JOIN LCM.User_Item UI ON W.ID = UI.ID_Item
    WHERE UI.ID_User = ?
    """, (user_id,))
    wards = cursor.fetchall()

    # Fetching chests owned by the user
    cursor.execute("""
    SELECT CH.ID, I.Name AS chest
    FROM LCM.Chest CH
    JOIN LCM.Item I ON CH.ID = I.ID
    JOIN LCM.User_Item UI ON CH.ID = UI.ID_Item
    WHERE UI.ID_User = ?
    """, (user_id,))
    chests = cursor.fetchall()

    return render_template('game.html', user_rank_points=user_rank_points, user_rp=user_rp,
                           champions=champions, skins=skins, wards=wards, chests=chests)

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
    
    cursor.execute("SELECT ID, Name, Category, Kingdom FROM GetChampionsByUser(?)", (user_id,))
    champions = cursor.fetchall()

    cursor.execute("SELECT ID, skin, championName FROM GetSkinsByUser(?)", (user_id,))
    skins = cursor.fetchall()

    cursor.execute("SELECT ID, ward FROM GetWardsByUser(?)", (user_id,))
    wards = cursor.fetchall()

    cursor.execute("SELECT ID, chest FROM GetChestsByUser(?)", (user_id,))
    chests = cursor.fetchall()
    
    return render_template('profile.html', champions=champions, skins=skins,wards=wards,chests=chests,user_be=user_be, user_rp=user_rp)

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

    cursor.execute("SELECT ID, Name, Category, Kingdom FROM GetChampionsByUser(?)",(user_id))
    champions = cursor.fetchall()

    cursor.execute("SELECT ID, skin, champion, rp_price FROM GetAvailableSkinsForUser(?)",(user_id))
    skins = cursor.fetchall()

    # Fetching wards
    cursor.execute("SELECT Name, ID, rp_price FROM GetAvailableWardsForUser(?)", (user_id))
    wards = cursor.fetchall()

    # Fetching chests
    cursor.execute("SELECT ID, Name, rp_price FROM dbo.GetChestsAndPrices()")
    chests = cursor.fetchall()

    return render_template('store.html', champions=champions, skins=skins, wards=wards, chests=chests, user_be=user_be, user_rp=user_rp)


@main_bp.route('/buy_champion_route', methods=['POST'])
def buy_champion_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    champion_id = data.get('champion_id')
    be_price = data.get('be_price')
    
    result = buy_champion(user_id, int(champion_id), int(be_price))
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
    
    purchaseRP(user_id,rp_amount)
    return jsonify({"status": "success", "message": f"{rp_amount} RP added successfully"})

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

@main_bp.route('/buy_ward_route', methods=['POST'])
def buy_ward_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    ward_id = data.get('ward_id')
    rp_price = data.get('rp_price')

    result = buy_ward(user_id, ward_id, rp_price)
    return jsonify(result)

@main_bp.route('/buy_chest_route', methods=['POST'])
def buy_chest_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    chest_id = data.get('chest_id')
    rp_price = data.get('rp_price')

    result = buy_chest(user_id, chest_id, rp_price)
    return jsonify(result)

@main_bp.route('/get_skins/<int:champion_id>')
def get_skins(champion_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT S.ID, S.Name AS skin_name
        FROM LCM.Skin S
        WHERE S.Champion_ID = ?
    """, (champion_id,))
    skins = cursor.fetchall()
    return jsonify(skins)  # Returning JSON response