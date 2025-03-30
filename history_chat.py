from database import get_db
from typing import NewType

UserID = NewType("UserID",int)

def save_chat_history(user_id, message, response):
    db = get_db()
    cursor = db.cursor()
    query = """
    INSERT INTO chat_history (user_id, message, response, timestamp)
    VALUES (?, ?, ?, GETDATE())
    """
    cursor.execute(query, (user_id, message, response))
    db.commit()

def get_chat_history(user_id):
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT top 5 message, response 
    FROM chat_history 
    WHERE user_id = ? 
    ORDER BY timestamp DESC 
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()