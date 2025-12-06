import json
import asyncio
import os

from dotenv import load_dotenv

from bot.domain.messenger import Messenger
from bot.domain.order_state import OrderState
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus

load_dotenv()


class OrderApprovalApprovedHandler(Handler):
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
        return callback_data == "order_approve"

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
            storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PAYMENT),
        )

        pizza_name = order_json.get("pizza_name", "Unknown")
        pizza_size = order_json.get("pizza_size", "Unknown")
        drink_name = order_json.get("drink_name", "Unknown")

        # Calculate prices (in kopecks for RUB)
        # Base prices - these can be customized
        pizza_prices = {
            "S (20cm)": 50000,  # 500.00 RUB
            "M (25cm)": 65000,  # 650.00 RUB
            "L (30cm)": 80000,  # 800.00 RUB
            "XL (35cm)": 95000,  # 950.00 RUB
        }
        drink_price = 10000  # 100.00 RUB (if drink is selected and not "No drinks")

        pizza_price = pizza_prices.get(pizza_size, 50000)
        prices = [
            {"label": f"Pizza: {pizza_name} ({pizza_size})", "amount": pizza_price}
        ]

        if drink_name:
            prices.append({"label": f"Drink: {drink_name}", "amount": drink_price})

        # Create order payload
        order_payload = json.dumps(
            {
                "telegram_id": telegram_id,
                "pizza_name": pizza_name,
                "pizza_size": pizza_size,
                "drink_name": drink_name,
            }
        )

        # Send invoice
        await messenger.send_invoice(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            title="Pizza Order",
            description=f"Pizza: {pizza_name}, Size: {pizza_size}, Drink: {drink_name}",
            payload=order_payload,
            provider_token=os.getenv("YOOKASSA_TOKEN"),
            currency="RUB",
            prices=prices,
        )

        return HandlerStatus.STOP
