from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def send_message(self, chat_id: int, text: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def get_updates(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def answer_callback_query(self, callback_query_id: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def delete_message(self, chat_id: int, message_id: int) -> dict:
        pass
