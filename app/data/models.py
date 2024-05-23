from .database import get_db

def create_user(username, email, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC CreateUser ?, ?, ?", (username, email, password))
    db.commit()

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GetUserByUsername(?)", (username,))
    user = cursor.fetchone()
    return user

def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GetUserByEmail(?)", (email,))
    user = cursor.fetchone()
    return user

def verify_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC VerifyUser ?, ?", (username, password))
    user = cursor.fetchone()
    return user

def buy_champion(user_id, champion_id, be_price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuyChampion ?, ?, ?", (user_id, champion_id, be_price))
    result = cursor.fetchone()
    db.commit()
    
    if result and result.Result == 'Success':
        return {"status": "success", "message": result.Message}
    else:
        return {"status": "error", "message": result.Message}

def buy_skin(user_id, skin_id, rp_price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuySkin ?, ?, ?", (user_id, skin_id, rp_price))
    result = cursor.fetchone()
    db.commit()

    if result and result.Result == 'Success':
        return {"status": "success", "message": result.Message}
    else:
        return {"status": "error", "message": result.Message}
    
def get_user_balance(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GetUserBalance(?)", user_id)
    balance = cursor.fetchone()
    return balance

def buy_ward(user_id, ward_id, rp_price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuyWard ?, ?, ?", (user_id, ward_id, rp_price))
    result = cursor.fetchone()
    db.commit()

    if result and result[0] == 'Success':
        return {"status": "success", "message": result[1]}
    else:
        return {"status": "error", "message": result[1] if result else "Unknown error occurred"}


def buy_chest(user_id, chest_id, rp_price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuyChest ?, ?, ?", (user_id, chest_id, rp_price))
    result = cursor.fetchone()
    db.commit()

    if result and result[0] == 'Success':
        return {"status": "success", "message": result[1]}
    else:
        return {"status": "error", "message": result[1] if result else "Unknown error occurred"}




def purchaseRP(user_id, rp_amount):
    db = get_db()
    cursor = db.cursor()
    result = cursor.execute("EXEC PurchaseRP ?,?",(user_id,rp_amount))
    result.fetchone()
    db.commit()

    if result and hasattr(result, 'Result') and hasattr(result, 'Message'):
        if result.Result == 'Success':
            return {"status": "success", "message": result.Message}
        else:
            return {"status": "error", "message": result.Message}
    else:
        return {"status": "error", "message": "An error occurred"}







