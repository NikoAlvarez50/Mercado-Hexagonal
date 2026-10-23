"""Entidades del dominio: reglas de negocio puras, sin dependencias externas."""
from dataclasses import dataclass, field
from typing import List

from app.domain.exceptions import InsufficientStockError, ValidationError


@dataclass
class User:
    id: str
    name: str
    email: str

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValidationError("El nombre es obligatorio")
        if not isinstance(self.email, str) or "@" not in self.email:
            raise ValidationError("El email no es válido")
        self.name = self.name.strip()
        self.email = self.email.strip().lower()


@dataclass
class Product:
    id: str
    name: str
    price: float

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValidationError("El nombre del producto es obligatorio")
        if isinstance(self.price, bool) or not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValidationError("El precio debe ser un número mayor que 0")
        self.name = self.name.strip()
        self.price = float(self.price)


@dataclass
class StockItem:
    product_id: str
    quantity: int

    def __post_init__(self):
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int) or self.quantity < 0:
            raise ValidationError("La cantidad debe ser un entero mayor o igual a 0")

    def ensure_available(self, amount: int) -> None:
        if amount > self.quantity:
            raise InsufficientStockError(
                f"Stock insuficiente para el producto {self.product_id}: "
                f"disponible {self.quantity}, solicitado {amount}"
            )

    def reserve(self, amount: int) -> None:
        self.ensure_available(amount)
        self.quantity -= amount


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    id: str
    user_id: str
    items: List[OrderItem] = field(default_factory=list)
    status: str = "CREATED"

    def __post_init__(self):
        if not self.items:
            raise ValidationError("El pedido debe tener al menos un ítem")

    @property
    def total(self) -> float:
        return round(sum(i.subtotal for i in self.items), 2)


@dataclass
class Notification:
    id: str
    user_id: str
    message: str
