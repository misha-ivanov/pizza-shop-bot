from bot.handlers.handler import Handler
from bot.handlers.update_database_logger import UpdateDatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_start import MessageStart
from bot.handlers.pizza_selection import PizzaSelection
from bot.handlers.pizza_size import PizzaSize
from bot.handlers.drink_selection import DrinkSelection


def get_handlers() -> list[Handler]:
    return [
        UpdateDatabaseLogger(),
        EnsureUserExists(),

        MessageStart(),
        PizzaSelection(),
        PizzaSize(),
        DrinkSelection(),
    ]