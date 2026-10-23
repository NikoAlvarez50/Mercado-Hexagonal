"""Pruebas de los servicios de aplicación y el dominio, sin Flask."""
import pytest

from app.domain.entities import Product, StockItem, User
from app.domain.exceptions import (
    ConflictError,
    InsufficientStockError,
    NotFoundError,
    ValidationError,
)


def test_user_normaliza_email_y_valida():
    assert User("1", " Ana ", "ANA@Mail.com").email == "ana@mail.com"
    with pytest.raises(ValidationError):
        User("1", "", "a@b.com")
    with pytest.raises(ValidationError):
        User("1", "Ana", "sin-arroba")


def test_producto_precio_positivo():
    with pytest.raises(ValidationError):
        Product("1", "Café", 0)


def test_stock_reserve():
    item = StockItem("p1", 3)
    item.reserve(2)
    assert item.quantity == 1
    with pytest.raises(InsufficientStockError):
        item.reserve(5)


def test_email_duplicado(container):
    container.users.register("Ana", "ana@mail.com")
    with pytest.raises(ConflictError):
        container.users.register("Otra", "ANA@mail.com")


def test_pedido_descuenta_stock_y_notifica(container):
    user = container.users.register("Ana", "ana@mail.com")
    product = container.products.create("Café", 10.5)
    container.inventory.set_stock(product.id, 5)

    order = container.orders.create_order(user.id, [{"product_id": product.id, "quantity": 2}])

    assert order.total == 21.0
    assert container.inventory.get_stock(product.id).quantity == 3
    assert len(container.notifications.list_for_user(user.id)) == 1


def test_pedido_sin_stock_no_reserva_nada(container):
    user = container.users.register("Ana", "ana@mail.com")
    a = container.products.create("A", 1)
    b = container.products.create("B", 2)
    container.inventory.set_stock(a.id, 5)
    container.inventory.set_stock(b.id, 1)

    with pytest.raises(InsufficientStockError):
        container.orders.create_order(
            user.id,
            [{"product_id": a.id, "quantity": 2}, {"product_id": b.id, "quantity": 3}],
        )
    assert container.inventory.get_stock(a.id).quantity == 5
    assert container.orders.list() == []


def test_pedido_usuario_inexistente(container):
    with pytest.raises(NotFoundError):
        container.orders.create_order("nope", [{"product_id": "x", "quantity": 1}])
