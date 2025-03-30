from database import get_db
from typing import NewType

UserID = NewType("UserID",int)

def save_chat_history(user_id:int,message:str,response:str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
INSERT INTO history_chat (id_usuario,u_message,response) values (?,?,?)
""",(int(user_id),str(message),str(response)))
    conn.commit()
    conn.close()


def get_chat_history(user_id, limit=5):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT top ? u_message, response FROM history_chat
        WHERE id_usuario = ?
        ORDER BY u_timestamp DESC;
    """, limit,(int(user_id)))
    history = cursor.fetchall()
    conn.close()
    return history