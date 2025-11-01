import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus


class DrinkSelection(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        
        if state != "WAIT_FOR_DRINKS":
            return False
        
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink_mapping = {
            "drink_mint_tea": "Mint Tea",
            "drink_black_tea": "Black Tea",
            "drink_latte": "Latte",
            "drink_black_coffee": "Black Coffee",
            "drink_spring_water": "Spring Water",
            "drink_fizzy_water": "Fizzy Water",
        }

        drink_name = drink_mapping.get(callback_data)
        order_json["drink_name"] = drink_name
        bot.database_client.update_user_order_json(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")

        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])

        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        return HandlerStatus.STOP