import json
import asyncio

from bot.domain.messenger import Messenger
from bot.domain.order_state import OrderState
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class OrderApprovalRestartHandler(Handler):
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

        if state != OrderState.WAIT_FOR_ORDER_APPROVE:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data == "order_restart"

    async def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        message_id = update["callback_query"]["message"]["message_id"]
        callback_query_id = update["callback_query"]["id"]

        await asyncio.gather(
            messenger.answer_callback_query(callback_query_id),
            messenger.delete_message(chat_id=chat_id, message_id=message_id),
            storage.clear_user_order_json(telegram_id),
            storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PIZZA_NAME),
        )

        new_order_text = """
🔄Let's try again!
Please choose pizza name:
"""

        await messenger.send_message(
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
