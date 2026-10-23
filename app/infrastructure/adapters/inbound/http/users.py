from flask import Blueprint, jsonify, request

from app.application.ports.inbound import UserServicePort
from app.infrastructure.adapters.inbound.http.common import to_dict


def create_blueprint(service: UserServicePort) -> Blueprint:
    bp = Blueprint("users", __name__, url_prefix="/users")

    @bp.post("")
    def register():
        body = request.get_json(silent=True) or {}
        user = service.register(body.get("name"), body.get("email"))
        return jsonify(to_dict(user)), 201

    @bp.get("")
    def list_users():
        return jsonify([to_dict(u) for u in service.list()])

    @bp.get("/<user_id>")
    def get_user(user_id):
        return jsonify(to_dict(service.get(user_id)))

    return bp
