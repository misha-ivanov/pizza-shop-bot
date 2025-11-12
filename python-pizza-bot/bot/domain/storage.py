from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def ensure_user_exists(self, telegram_id: int) -> None:
        pass

    @abstractmethod
    def clear_user_state_and_order_json(self, telegram_id: int) -> None:
        pass

    @abstractmethod
    def clear_user_order_json(self, telegram_id: int) -> None:
        pass

    @abstractmethod
    def clear_user_state(self, telegram_id: int) -> None:
        pass

    @abstractmethod
    def update_user_order_json(self, telegram_id: int, order_json: dict) -> None:
        pass

    @abstractmethod
    def update_user_state(self, telegram_id: int, state: str) -> None:
        pass

    @abstractmethod
    def persist_update(self, update: dict) -> None:
        pass

    @abstractmethod
    def recreate_database(self) -> None:
        pass

    @abstractmethod
    def get_user(self, telegram_id: int) -> dict:
        pass
