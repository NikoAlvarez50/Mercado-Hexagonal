"""Utilidades compartidas por los adaptadores HTTP: serialización y manejo de errores."""
from dataclasses import asdict
from typing import Any

from flask import Flask, jsonify

from app.domain.exceptions import (
    ConflictError,
    DomainError,
    InsufficientStockError,
    NotFoundError,
    ValidationError,
)


def to_dict(entity: Any) -> dict:
    data = asdict(entity)
    if hasattr(entity, "total"):
        data["total"] = entity.total
    return data


def register_error_handlers(app: Flask) -> None:
    mapping = {
        ValidationError: 400,
        NotFoundError: 404,
        ConflictError: 409,
        InsufficientStockError: 409,
    }

    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError):
        status = next((code for cls, code in mapping.items() if isinstance(error, cls)), 400)
        return jsonify({"error": type(error).__name__, "message": str(error)}), status

    @app.errorhandler(404)
    def handle_404(_):
        return jsonify({"error": "NotFound", "message": "Ruta no encontrada"}), 404

    @app.errorhandler(405)
    def handle_405(_):
        return jsonify({"error": "MethodNotAllowed", "message": "Método no permitido"}), 405
