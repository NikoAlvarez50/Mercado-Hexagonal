"""Pruebas del adaptador web: interfaz, Swagger y especificación OpenAPI."""
import re


def test_index_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.mimetype == "text/html"
    assert "Mercado hexagonal" in resp.get_data(as_text=True)


def test_docs_y_openapi(client):
    assert client.get("/docs").status_code == 200
    spec = client.get("/openapi.json").get_json()
    assert spec["openapi"].startswith("3.")
    assert "/orders" in spec["paths"]


def test_spec_cubre_todas_las_rutas_de_la_api(client):
    spec_paths = set(client.get("/openapi.json").get_json()["paths"])
    rules = client.application.url_map.iter_rules()
    api_paths = {
        re.sub(r"<([^>]+)>", r"{\1}", r.rule)
        for r in rules
        if r.endpoint != "static" and not r.endpoint.startswith("web.")
    }
    assert api_paths <= spec_paths


def test_api_sigue_respondiendo_404_json(client):
    resp = client.get("/ruta-que-no-existe")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "NotFound"
