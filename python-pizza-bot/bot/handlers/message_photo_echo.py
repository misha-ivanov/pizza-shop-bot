from bot.handler import Handler
import bot.telegram_client

class MessagePhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]

    def handle(self, update: dict) -> bool:
        photos=update["message"]["photo"]
        max_photo=max(photos, key=lambda p: p["file_size"])
        max_photo_id=max_photo["file_id"]

        bot.telegram_client.sendPhoto(
            chat_id=update["message"]["chat"]["id"],
            photo=max_photo_id,
        )
        return False