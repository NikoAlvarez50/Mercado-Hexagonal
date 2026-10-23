"""Pruebas de extremo a extremo a través del adaptador HTTP."""


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_flujo_completo(client):
    user = client.post("/users", json={"name": "Ana", "email": "ana@mail.com"})
    assert user.status_code == 201
    user_id = user.get_json()["id"]

    product = client.post("/products", json={"name": "Café", "price": 12.5})
    assert product.status_code == 201
    product_id = product.get_json()["id"]

    stock = client.put(f"/inventory/{product_id}", json={"quantity": 10})
    assert stock.get_json()["quantity"] == 10

    order = client.post(
        "/orders", json={"user_id": user_id, "items": [{"product_id": product_id, "quantity": 4}]}
    )
    assert order.status_code == 201
    assert order.get_json()["total"] == 50.0

    assert client.get(f"/inventory/{product_id}").get_json()["quantity"] == 6
    assert len(client.get(f"/notifications/{user_id}").get_json()) == 1
    assert len(client.get("/orders").get_json()) == 1
    assert client.get(f"/orders/{order.get_json()['id']}").status_code == 200


def test_errores_http(client):
    assert client.post("/users", json={"name": "", "email": "x"}).status_code == 400
    assert client.get("/users/inexistente").status_code == 404
    client.post("/users", json={"name": "Ana", "email": "ana@mail.com"})
    assert client.post("/users", json={"name": "Ana", "email": "ana@mail.com"}).status_code == 409


def test_stock_insuficiente_409(client):
    user_id = client.post("/users", json={"name": "Ana", "email": "a@a.com"}).get_json()["id"]
    product_id = client.post("/products", json={"name": "X", "price": 1}).get_json()["id"]
    client.put(f"/inventory/{product_id}", json={"quantity": 1})
    resp = client.post(
        "/orders", json={"user_id": user_id, "items": [{"product_id": product_id, "quantity": 2}]}
    )
    assert resp.status_code == 409
    assert resp.get_json()["error"] == "InsufficientStockError"
