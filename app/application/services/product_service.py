"""Servicio 2: Productos."""
from typing import List

from app.application.ports.inbound import ProductServicePort
from app.application.ports.outbound import IdGenerator, ProductRepository
from app.domain.entities import Product
from app.domain.exceptions import NotFoundError


class ProductService(ProductServicePort):
    def __init__(self, repository: ProductRepository, ids: IdGenerator):
        self._repo = repository
        self._ids = ids

    def create(self, name: str, price: float) -> Product:
        product = Product(id=self._ids.new_id(), name=name, price=price)
        return self._repo.save(product)

    def get(self, product_id: str) -> Product:
        product = self._repo.get(product_id)
        if product is None:
            raise NotFoundError(f"Producto {product_id} no encontrado")
        return product

    def list(self) -> List[Product]:
        return self._repo.list()
