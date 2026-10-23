"""Puertos de entrada (driving ports): lo que la aplicación ofrece al exterior."""
from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import Notification, Order, Product, StockItem, User


class UserServicePort(ABC):
    @abstractmethod
    def register(self, name: str, email: str) -> User: ...

    @abstractmethod
    def get(self, user_id: str) -> User: ...

    @abstractmethod
    def list(self) -> List[User]: ...


class ProductServicePort(ABC):
    @abstractmethod
    def create(self, name: str, price: float) -> Product: ...

    @abstractmethod
    def get(self, product_id: str) -> Product: ...

    @abstractmethod
    def list(self) -> List[Product]: ...


class InventoryServicePort(ABC):
    @abstractmethod
    def set_stock(self, product_id: str, quantity: int) -> StockItem: ...

    @abstractmethod
    def get_stock(self, product_id: str) -> StockItem: ...

    @abstractmethod
    def reserve(self, product_id: str, quantity: int) -> StockItem: ...


class OrderServicePort(ABC):
    @abstractmethod
    def create_order(self, user_id: str, items: List[dict]) -> Order: ...

    @abstractmethod
    def get(self, order_id: str) -> Order: ...

    @abstractmethod
    def list(self) -> List[Order]: ...


class NotificationServicePort(ABC):
    @abstractmethod
    def notify(self, user_id: str, message: str) -> Notification: ...

    @abstractmethod
    def list_for_user(self, user_id: str) -> List[Notification]: ...
