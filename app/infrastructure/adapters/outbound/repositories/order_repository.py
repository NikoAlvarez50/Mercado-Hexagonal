from typing import List, Optional

from app.application.ports.outbound import OrderRepository
from app.domain.entities import Order
from app.infrastructure.adapters.outbound.repositories.base import InMemoryStore


class InMemoryOrderRepository(InMemoryStore[Order], OrderRepository):
    def save(self, order: Order) -> Order:
        return self._put(order.id, order)

    def get(self, order_id: str) -> Optional[Order]:
        return self._find(order_id)

    def list(self) -> List[Order]:
        return self._all()
