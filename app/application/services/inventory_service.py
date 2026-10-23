"""Servicio 3: Inventario."""
from app.application.ports.inbound import InventoryServicePort, ProductServicePort
from app.application.ports.outbound import InventoryRepository
from app.domain.entities import StockItem


class InventoryService(InventoryServicePort):
    def __init__(self, repository: InventoryRepository, products: ProductServicePort):
        self._repo = repository
        self._products = products

    def set_stock(self, product_id: str, quantity: int) -> StockItem:
        self._products.get(product_id)  # lanza NotFoundError si no existe
        return self._repo.save(StockItem(product_id=product_id, quantity=quantity))

    def get_stock(self, product_id: str) -> StockItem:
        self._products.get(product_id)
        item = self._repo.get(product_id)
        return item if item is not None else StockItem(product_id=product_id, quantity=0)

    def reserve(self, product_id: str, quantity: int) -> StockItem:
        item = self.get_stock(product_id)
        item.reserve(quantity)
        return self._repo.save(item)
