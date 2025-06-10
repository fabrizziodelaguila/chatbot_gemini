import json
import os

HISTORY_FILE = "chat_history.json"

def load_data():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_chat_history(user_id):
    data = load_data()
    return data.get(str(user_id), [])

def save_chat_history(user_id, question, answer):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = []
    data[uid].append([question, answer])
    save_data(data)
