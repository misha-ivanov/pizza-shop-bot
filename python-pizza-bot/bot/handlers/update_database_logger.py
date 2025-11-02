import sqlite3
import os
import json
from bot.handlers.handler import Handler, HandlerStatus


class UpdateDatabaseLogger(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        return True

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        connection = sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH"))
        with connection:
            data = []
            data.append((json.dumps(update, ensure_ascii=False, indent=3),))
            connection.executemany(
                "INSERT INTO telegram_updates (payload) VALUES (?)",
                data,
            )
        connection.close()
        return HandlerStatus.CONTINUE
