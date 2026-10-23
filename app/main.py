"""Fábrica de la aplicación Flask (adaptador de entrada HTTP)."""
from typing import Optional

from flask import Flask, jsonify

from app.infrastructure.adapters.inbound.http import (
    inventory,
    notifications,
    orders,
    products,
    users,
)
from app.infrastructure.adapters.inbound.http.common import register_error_handlers
from app.infrastructure.adapters.inbound.web import ui
from app.infrastructure.container import Container, build_container


def create_app(container: Optional[Container] = None) -> Flask:
    container = container or build_container()
    app = Flask(__name__)

    app.register_blueprint(users.create_blueprint(container.users))
    app.register_blueprint(products.create_blueprint(container.products))
    app.register_blueprint(inventory.create_blueprint(container.inventory))
    app.register_blueprint(orders.create_blueprint(container.orders))
    app.register_blueprint(notifications.create_blueprint(container.notifications))
    app.register_blueprint(ui.create_blueprint())  # interfaz web "/" y Swagger "/docs"
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
