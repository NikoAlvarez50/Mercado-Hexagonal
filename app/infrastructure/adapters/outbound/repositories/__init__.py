"""Repositorios en memoria (adaptadores de salida), un archivo por repositorio.

Para pasar a una base de datos real, se crea una carpeta/archivo equivalente
(p. ej. sql_user_repository.py) que implemente los mismos puertos y se cambia
únicamente el contenedor de dependencias.
"""
from app.infrastructure.adapters.outbound.repositories.inventory_repository import (
    InMemoryInventoryRepository,
)
from app.infrastructure.adapters.outbound.repositories.notification_repository import (
    InMemoryNotificationRepository,
)
from app.infrastructure.adapters.outbound.repositories.order_repository import (
    InMemoryOrderRepository,
)
from app.infrastructure.adapters.outbound.repositories.product_repository import (
    InMemoryProductRepository,
)
from app.infrastructure.adapters.outbound.repositories.user_repository import (
    InMemoryUserRepository,
)

__all__ = [
    "InMemoryInventoryRepository",
    "InMemoryNotificationRepository",
    "InMemoryOrderRepository",
    "InMemoryProductRepository",
    "InMemoryUserRepository",
]
