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
    cursor.execute("EXEC VerifyUser ?jonyboi, ?", (username, password))
    user = cursor.fetchone()
    return user             

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







