import json
import os
from datetime import datetime

HISTORY_FILE = "chat_history.json"

def save_message(user, message, is_bot):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "timestamp": datetime.now().isoformat(),
        "sender": "bot" if is_bot else "user",
        "message": message
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
