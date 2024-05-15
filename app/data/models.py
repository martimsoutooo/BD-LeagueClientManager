from .database import get_db

def create_user(ID, Name, Email, Password, Rank_Points, BE, RP):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO LCM.[User] (ID,Name, Email, Password, Rank_Points,BE,RP) VALUES (?, ?, ?, ?, ?, ?)",
        (ID, Name, Email, Password, Rank_Points, BE, RP)
    )
    db.commit()

def get_user_by_username(Name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT ID, Name, Email, password FROM LCM.[User] WHERE Name = ?",
        (Name,)
    )
    return cursor.fetchone()

def get_user_by_email(Email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT ID, Name, Email, Password FROM LCM.[User] WHERE email = ?",
        (Email,)
    )
    return cursor.fetchone()


