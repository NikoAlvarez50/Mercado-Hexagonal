from flask import Blueprint, jsonify, request

from app.application.ports.inbound import OrderServicePort
from app.infrastructure.adapters.inbound.http.common import to_dict


def create_blueprint(service: OrderServicePort) -> Blueprint:
    bp = Blueprint("orders", __name__, url_prefix="/orders")

    @bp.post("")
    def create_order():
        body = request.get_json(silent=True) or {}
        order = service.create_order(body.get("user_id"), body.get("items"))
        return jsonify(to_dict(order)), 201

    @bp.get("")
    def list_orders():
        return jsonify([to_dict(o) for o in service.list()])

    @bp.get("/<order_id>")
    def get_order(order_id):
        return jsonify(to_dict(service.get(order_id)))

    return bp
