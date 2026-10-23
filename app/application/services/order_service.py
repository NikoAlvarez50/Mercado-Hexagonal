"""Servicio 4: Pedidos. Orquesta usuarios, productos, inventario y notificaciones."""
from typing import List

from app.application.ports.inbound import (
    InventoryServicePort,
    NotificationServicePort,
    OrderServicePort,
    ProductServicePort,
    UserServicePort,
)
from app.application.ports.outbound import IdGenerator, OrderRepository
from app.domain.entities import Order, OrderItem
from app.domain.exceptions import NotFoundError, ValidationError


class OrderService(OrderServicePort):
    def __init__(
        self,
        repository: OrderRepository,
        users: UserServicePort,
        products: ProductServicePort,
        inventory: InventoryServicePort,
        notifications: NotificationServicePort,
        ids: IdGenerator,
    ):
        self._repo = repository
        self._users = users
        self._products = products
        self._inventory = inventory
        self._notifications = notifications
        self._ids = ids

    def create_order(self, user_id: str, items: List[dict]) -> Order:
        self._users.get(user_id)
        if not isinstance(items, list) or not items:
            raise ValidationError("El pedido debe tener al menos un ítem")

        # 1) Validar y construir ítems con el precio vigente
        order_items: List[OrderItem] = []
        for raw in items:
            product_id = raw.get("product_id") if isinstance(raw, dict) else None
            quantity = raw.get("quantity") if isinstance(raw, dict) else None
            if not product_id:
                raise ValidationError("Cada ítem requiere product_id")
            if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
                raise ValidationError("La cantidad debe ser un entero mayor que 0")
            product = self._products.get(product_id)
            order_items.append(OrderItem(product.id, quantity, product.price))

        # 2) Verificar stock de todo el pedido antes de reservar
        for item in order_items:
            self._inventory.get_stock(item.product_id).ensure_available(item.quantity)

        # 3) Reservar, guardar y notificar
        for item in order_items:
            self._inventory.reserve(item.product_id, item.quantity)
        order = self._repo.save(Order(id=self._ids.new_id(), user_id=user_id, items=order_items))
        self._notifications.notify(
            user_id, f"Tu pedido {order.id} fue creado. Total: {order.total:.2f}"
        )
        return order

    def get(self, order_id: str) -> Order:
        order = self._repo.get(order_id)
        if order is None:
            raise NotFoundError(f"Pedido {order_id} no encontrado")
        return order

    def list(self) -> List[Order]:
        return self._repo.list()
