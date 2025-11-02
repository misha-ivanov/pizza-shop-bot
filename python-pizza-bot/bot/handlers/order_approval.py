import json

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class OrderApproval(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("approve_")

    def handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        messenger.answer_callback_query(update["callback_query"]["id"])

        messenger.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "approve_true":
            storage.update_user_state(telegram_id, "ORDER_FINISHED")

            pizza_name = order_json.get("pizza_name", "-")
            pizza_size = order_json.get("pizza_size", "-")
            drink_name = order_json.get("drink_name", "-")

            final_order = f"""
🧡Thanks for your order!
                
*Pizza:* {pizza_name}
*Size:* {pizza_size}
*Drink:* {drink_name}

Text "/start" for new order.
"""

            messenger.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=final_order,
                parse_mode="Markdown",
            )

        else:
            # refresh client data
            storage.clear_user_state_and_order_json(telegram_id)
            storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            new_order_text = """
🔄Let's try again!
Please choose pizza name:
"""

            messenger.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=new_order_text,
                parse_mode="Markdown",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Margherita",
                                    "callback_data": "pizza_margherita",
                                },
                                {
                                    "text": "Pepperoni",
                                    "callback_data": "pizza_pepperoni",
                                },
                            ],
                            [
                                {
                                    "text": "Carbonara",
                                    "callback_data": "pizza_carbonara",
                                },
                                {
                                    "text": "Parmigiana",
                                    "callback_data": "pizza_parmigiana",
                                },
                            ],
                            [
                                {"text": "Diavola", "callback_data": "pizza_diavola"},
                                {
                                    "text": "Gorgonzola",
                                    "callback_data": "pizza_gorgonzola",
                                },
                            ],
                        ],
                    },
                ),
            )
        return HandlerStatus.STOP
