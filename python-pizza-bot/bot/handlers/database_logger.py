import sqlite3
import os
import json
from bot.handler import Handler

class DatabaseLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and ("text" in update["message"] or "photo" in update["message"])

    def handle(self, update: dict) -> bool:
        connection = sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH'))
        with connection:
            data = []
            data.append((json.dumps(update, ensure_ascii=False, indent=3),))
            connection.executemany(
                "INSERT INTO telegram_updates (payload) VALUES (?)",
                data,
            )
        connection.close()
        return True