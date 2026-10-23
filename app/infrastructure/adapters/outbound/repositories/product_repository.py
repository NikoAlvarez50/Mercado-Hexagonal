from typing import List, Optional

from app.application.ports.outbound import ProductRepository
from app.domain.entities import Product
from app.infrastructure.adapters.outbound.repositories.base import InMemoryStore


class InMemoryProductRepository(InMemoryStore[Product], ProductRepository):
    def save(self, product: Product) -> Product:
        return self._put(product.id, product)

    def get(self, product_id: str) -> Optional[Product]:
        return self._find(product_id)

    def list(self) -> List[Product]:
        return self._all()
