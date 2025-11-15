from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def send_message(self, chat_id: int, text: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def send_invoice(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list,
        **kwargs,
    ) -> dict:
        pass

    @abstractmethod
    def answer_pre_checkout_query(
        self, pre_checkout_query_id: str, ok: bool, **kwargs
    ) -> dict:
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
