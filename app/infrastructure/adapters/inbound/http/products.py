from flask import Blueprint, jsonify, request

from app.application.ports.inbound import ProductServicePort
from app.infrastructure.adapters.inbound.http.common import to_dict


def create_blueprint(service: ProductServicePort) -> Blueprint:
    bp = Blueprint("products", __name__, url_prefix="/products")

    @bp.post("")
    def create():
        body = request.get_json(silent=True) or {}
        product = service.create(body.get("name"), body.get("price"))
        return jsonify(to_dict(product)), 201

    @bp.get("")
    def list_products():
        return jsonify([to_dict(p) for p in service.list()])

    @bp.get("/<product_id>")
    def get_product(product_id):
        return jsonify(to_dict(service.get(product_id)))

    return bp
