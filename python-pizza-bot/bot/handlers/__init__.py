from bot.handlers.handler import Handler
from bot.handlers.update_database_logger import UpdateDatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_echo import MessageEcho
from bot.handlers.message_photo_echo import MessagePhotoEcho


def get_handlers() -> list[Handler]:
    return [
        UpdateDatabaseLogger(),
        EnsureUserExists(),
        MessageEcho(),
        MessagePhotoEcho(),
    ]