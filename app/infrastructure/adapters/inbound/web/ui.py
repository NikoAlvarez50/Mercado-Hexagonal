"""Adaptador de entrada web: interfaz HTML en "/" y documentación Swagger en "/docs"."""
from flask import Blueprint, jsonify, render_template

from app.infrastructure.adapters.inbound.web.openapi import build_spec


def create_blueprint() -> Blueprint:
    bp = Blueprint("web", __name__, template_folder="templates")

    @bp.get("/")
    def index():
        return render_template("index.html")

    @bp.get("/docs")
    def docs():
        return render_template("docs.html")

    @bp.get("/openapi.json")
    def openapi():
        return jsonify(build_spec())

    return bp
