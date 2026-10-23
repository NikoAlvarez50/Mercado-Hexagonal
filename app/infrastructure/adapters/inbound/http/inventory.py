from flask import Blueprint, jsonify, request

from app.application.ports.inbound import InventoryServicePort
from app.infrastructure.adapters.inbound.http.common import to_dict


def create_blueprint(service: InventoryServicePort) -> Blueprint:
    bp = Blueprint("inventory", __name__, url_prefix="/inventory")

    @bp.put("/<product_id>")
    def set_stock(product_id):
        body = request.get_json(silent=True) or {}
        item = service.set_stock(product_id, body.get("quantity"))
        return jsonify(to_dict(item))

    @bp.get("/<product_id>")
    def get_stock(product_id):
        return jsonify(to_dict(service.get_stock(product_id)))

    return bp
