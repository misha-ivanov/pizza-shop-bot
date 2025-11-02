from bot.dispatcher import Dispatcher
from bot.handlers.pizza_size import PizzaSize

from tests.mocks import Mock


def test_pizza_size_handler():
    test_update = {
        "update_id": 11111111,
        "callback_query": {
            "id": "11",
            "from": {
                "id": 10,
                "is_bot": False,
                "first_name": "Mike",
                "last_name": "Ivanov",
                "username": "Mirok_now",
                "language_code": "ru",
            },
            "message": {
                "message_id": 256,
                "from": {
                    "id": 1,
                    "is_bot": True,
                    "first_name": "Иванов М.И.",
                    "username": "unn_ivanov_bot",
                },
                "chat": {
                    "id": 10,
                    "first_name": "Mike",
                    "last_name": "Ivanov",
                    "username": "Mirok_now",
                    "type": "private",
                },
                "date": 1762092272,
                "text": "☕Please choose some drinks",
                "reply_markup": {
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
            },
            "chat_instance": "6405103211159057168",
            "data": "size_xl",
        },
    }

    update_user_order_json_called = False
    update_user_state_called = False
    answer_callback_query_called = False
    delete_message_called = False

    def update_user_order_json(telegram_id: int, order_json: dict) -> None:
        assert telegram_id == 10
        assert order_json == {"pizza_name": "Parmigiana", "pizza_size": "XL (35cm)"}

        nonlocal update_user_order_json_called
        update_user_order_json_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 10
        assert state == "WAIT_FOR_DRINKS"

        nonlocal update_user_state_called
        update_user_state_called = True

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 10
        return {
            "state": "WAIT_FOR_PIZZA_SIZE",
            "order_json": '{"pizza_name": "Parmigiana"}',
        }

    send_message_calls = []

    def send_message(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 10
        send_message_calls.append({"text": text, "kwargs": kwargs})
        return {"ok": True}

    def answer_callback_query(callback_query_id: str) -> dict:
        assert callback_query_id == "11"
        nonlocal answer_callback_query_called
        answer_callback_query_called = True
        return {"ok": True}

    def delete_message(chat_id: int, message_id: int) -> dict:
        assert chat_id == 10
        assert message_id == 256
        nonlocal delete_message_called
        delete_message_called = True
        return {"ok": True}

    mock_storage = Mock(
        {
            "update_user_order_json": update_user_order_json,
            "update_user_state": update_user_state,
            "get_user": get_user,
        }
    )
    mock_messenger = Mock(
        {
            "send_message": send_message,
            "answer_callback_query": answer_callback_query,
            "delete_message": delete_message,
        }
    )

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handler(PizzaSize())

    dispatcher.dispatch(test_update)

    assert update_user_order_json_called
    assert update_user_state_called
    assert answer_callback_query_called
    assert delete_message_called

    assert len(send_message_calls) == 1
    assert send_message_calls[0]["text"] == "☕Please choose some drinks"
