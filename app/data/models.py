from .database import get_db

def create_user(Name, Email, Password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO LCM.[User] (Name, Email, Password) VALUES (?, ?, ?)",
        (Name, Email, Password)
    )
    db.commit()

def get_user_by_username(Name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT ID, Name, Email, Password FROM LCM.[User] WHERE Name = ?",
        (Name,)
    )
    return cursor.fetchone()

def get_user_by_email(Email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT ID, Name, Email, Password FROM LCM.[User] WHERE Email = ?",
        (Email,)
    )
    return cursor.fetchone()



