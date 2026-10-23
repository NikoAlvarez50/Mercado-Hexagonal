"""Puertos de salida (driven ports): lo que la aplicación necesita del exterior."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Notification, Order, Product, StockItem, User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def get(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def list(self) -> List[User]: ...


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product: ...

    @abstractmethod
    def get(self, product_id: str) -> Optional[Product]: ...

    @abstractmethod
    def list(self) -> List[Product]: ...


class InventoryRepository(ABC):
    @abstractmethod
    def save(self, item: StockItem) -> StockItem: ...

    @abstractmethod
    def get(self, product_id: str) -> Optional[StockItem]: ...


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order: ...

    @abstractmethod
    def get(self, order_id: str) -> Optional[Order]: ...

    @abstractmethod
    def list(self) -> List[Order]: ...


class NotificationRepository(ABC):
    @abstractmethod
    def save(self, notification: Notification) -> Notification: ...

    @abstractmethod
    def list_for_user(self, user_id: str) -> List[Notification]: ...


class NotificationSender(ABC):
    """Canal de envío (email, SMS, push...)."""

    @abstractmethod
    def send(self, user: User, message: str) -> None: ...


class IdGenerator(ABC):
    @abstractmethod
    def new_id(self) -> str: ...
