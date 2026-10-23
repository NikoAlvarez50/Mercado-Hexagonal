from typing import Optional

from app.application.ports.outbound import InventoryRepository
from app.domain.entities import StockItem
from app.infrastructure.adapters.outbound.repositories.base import InMemoryStore


class InMemoryInventoryRepository(InMemoryStore[StockItem], InventoryRepository):
    def save(self, item: StockItem) -> StockItem:
        return self._put(item.product_id, item)

    def get(self, product_id: str) -> Optional[StockItem]:
        return self._find(product_id)
