from bot.database_client import ensure_user_exists
from bot.handlers.handler import Handler, HandlerStatus

class EnsureUserExists (Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "from" in update ["message"]

    def handle(self, update: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]
        ensure_user_exists(telegram_id)
        return HandlerStatus.CONTINUE