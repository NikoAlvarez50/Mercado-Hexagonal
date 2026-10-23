"""Raíz de composición: aquí (y solo aquí) se conectan puertos con adaptadores."""
from dataclasses import dataclass

from app.application.ports.inbound import (
    InventoryServicePort,
    NotificationServicePort,
    OrderServicePort,
    ProductServicePort,
    UserServicePort,
)
from app.application.services.inventory_service import InventoryService
from app.application.services.notification_service import NotificationService
from app.application.services.order_service import OrderService
from app.application.services.product_service import ProductService
from app.application.services.user_service import UserService
from app.infrastructure.adapters.outbound.repositories import (
    InMemoryInventoryRepository,
    InMemoryNotificationRepository,
    InMemoryOrderRepository,
    InMemoryProductRepository,
    InMemoryUserRepository,
)
from app.infrastructure.adapters.outbound.misc_adapters import LogNotificationSender, UuidGenerator


@dataclass
class Container:
    users: UserServicePort
    products: ProductServicePort
    inventory: InventoryServicePort
    orders: OrderServicePort
    notifications: NotificationServicePort


def build_container() -> Container:
    ids = UuidGenerator()

    users = UserService(InMemoryUserRepository(), ids)
    products = ProductService(InMemoryProductRepository(), ids)
    inventory = InventoryService(InMemoryInventoryRepository(), products)
    notifications = NotificationService(
        InMemoryNotificationRepository(), LogNotificationSender(), users, ids
    )
    orders = OrderService(
        InMemoryOrderRepository(), users, products, inventory, notifications, ids
    )
    return Container(users, products, inventory, orders, notifications)
