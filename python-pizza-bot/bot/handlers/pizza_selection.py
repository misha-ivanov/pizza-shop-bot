import json
import asyncio

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.domain.order_state import OrderState


class PizzaSelection(Handler):
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

        if state != OrderState.WAIT_FOR_PIZZA_NAME:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    async def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        message_id = update["callback_query"]["message"]["message_id"]
        callback_query_id = update["callback_query"]["id"]

        await asyncio.gather(
            storage.update_user_order_json(telegram_id, {"pizza_name": pizza_name}),
            storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PIZZA_SIZE),
            messenger.answer_callback_query(callback_query_id),
        )

        await asyncio.gather(
            messenger.delete_message(chat_id=chat_id, message_id=message_id),
            messenger.send_message(
                chat_id=chat_id,
                text="🔎Please choose pizza size",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {"text": "S (20cm)", "callback_data": "size_s"},
                                {"text": "M (25cm)", "callback_data": "size_m"},
                            ],
                            [
                                {"text": "L (30cm)", "callback_data": "size_l"},
                                {"text": "XL (35cm)", "callback_data": "size_xl"},
                            ],
                        ],
                    },
                ),
            ),
        )
        return HandlerStatus.STOP
