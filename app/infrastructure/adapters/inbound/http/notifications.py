from flask import Blueprint, jsonify, request

from app.application.ports.inbound import NotificationServicePort
from app.infrastructure.adapters.inbound.http.common import to_dict


def create_blueprint(service: NotificationServicePort) -> Blueprint:
    bp = Blueprint("notifications", __name__, url_prefix="/notifications")

    @bp.post("/<user_id>")
    def send(user_id):
        body = request.get_json(silent=True) or {}
        notification = service.notify(user_id, body.get("message"))
        return jsonify(to_dict(notification)), 201

    @bp.get("/<user_id>")
    def list_for_user(user_id):
        return jsonify([to_dict(n) for n in service.list_for_user(user_id)])

    return bp
