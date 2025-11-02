import json

import bot.telegram_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus


class PizzaSize(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_s": "S (20cm)",
            "size_m": "M (25cm)",
            "size_l": "L (30cm)",
            "size_xl": "XL (35cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        order_json["pizza_size"] = pizza_size
        bot.database_client.update_user_order_json(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_DRINKS")

        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])

        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        bot.telegram_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="☕Please choose some drinks",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Mint Tea", "callback_data": "drink_mint_tea"},
                            {"text": "Black Tea", "callback_data": "drink_black_tea"},
                        ],
                        [
                            {"text": "Latte", "callback_data": "drink_latte"},
                            {
                                "text": "Black Coffee",
                                "callback_data": "drink_black_coffee",
                            },
                        ],
                        [
                            {
                                "text": "Spring Water",
                                "callback_data": "drink_spring_water",
                            },
                            {
                                "text": "Fizzy Water",
                                "callback_data": "drink_fizzy_water",
                            },
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
