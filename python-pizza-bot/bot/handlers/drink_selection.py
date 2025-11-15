import json

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.domain.order_state import OrderState


class DrinkSelection(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != OrderState.WAIT_FOR_DRINKS:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
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

        drink_name = drink_mapping.get(callback_data, "Not in menu")
        order_json["drink_name"] = drink_name
        storage.update_user_order_json(telegram_id, order_json)
        storage.update_user_state(telegram_id, OrderState.WAIT_FOR_ORDER_APPROVE)

        messenger.answer_callback_query(update["callback_query"]["id"])

        messenger.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        # Finalize the order and parse it into string
        pizza_name = order_json.get("pizza_name", "-")
        pizza_size = order_json.get("pizza_size", "-")
        drink_name = order_json.get("drink_name", "-")

        final_order = f"""
🤓Please, check the order and approve it if everything is fine:
*Pizza:* {pizza_name}
*Size:* {pizza_size}
*Drink:* {drink_name}
"""

        messenger.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=final_order,
            parse_mode="Markdown",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Approve", "callback_data": "order_approve"},
                        ],
                        [
                            {"text": "Start again", "callback_data": "order_restart"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
