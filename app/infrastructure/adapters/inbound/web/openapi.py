"""Especificación OpenAPI 3.0 de la API (se sirve en /openapi.json y se muestra en /docs)."""

_ERRORS = {
    "400": "Datos inválidos (ValidationError)",
    "404": "Recurso no encontrado (NotFoundError)",
    "409": "Conflicto: email duplicado o stock insuficiente",
}


def _ref(name):
    return {"$ref": f"#/components/schemas/{name}"}


def _array(name):
    return {"type": "array", "items": _ref(name)}


def _json(schema):
    return {"application/json": {"schema": schema}}


def _path_param(name):
    return {"name": name, "in": "path", "required": True, "schema": {"type": "string"}}


def _op(tag, summary, ok_schema, ok_code="200", body=None, params=(), errors=()):
    operation = {"tags": [tag], "summary": summary, "responses": {}}
    if params:
        operation["parameters"] = [_path_param(p) for p in params]
    if body:
        operation["requestBody"] = {"required": True, "content": _json(_ref(body))}
    operation["responses"][ok_code] = {"description": "OK", "content": _json(ok_schema)}
    for code in errors:
        operation["responses"][code] = {"description": _ERRORS[code], "content": _json(_ref("Error"))}
    return operation


def _obj(properties, required=None, example=None):
    schema = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    if example:
        schema["example"] = example
    return schema


_STR = {"type": "string"}
_INT = {"type": "integer"}
_NUM = {"type": "number"}


def build_spec():
    schemas = {
        "Error": _obj({"error": _STR, "message": _STR}),
        "User": _obj({"id": _STR, "name": _STR, "email": _STR}),
        "UserInput": _obj({"name": _STR, "email": _STR}, ["name", "email"],
                          {"name": "Ana Pérez", "email": "ana@mail.com"}),
        "Product": _obj({"id": _STR, "name": _STR, "price": _NUM}),
        "ProductInput": _obj({"name": _STR, "price": _NUM}, ["name", "price"],
                             {"name": "Café", "price": 12.5}),
        "StockItem": _obj({"product_id": _STR, "quantity": _INT}),
        "StockInput": _obj({"quantity": _INT}, ["quantity"], {"quantity": 10}),
        "OrderItemInput": _obj({"product_id": _STR, "quantity": _INT}, ["product_id", "quantity"]),
        "OrderItem": _obj({"product_id": _STR, "quantity": _INT, "unit_price": _NUM}),
        "OrderInput": _obj(
            {"user_id": _STR, "items": _array("OrderItemInput")}, ["user_id", "items"],
            {"user_id": "ID_DEL_USUARIO", "items": [{"product_id": "ID_DEL_PRODUCTO", "quantity": 2}]},
        ),
        "Order": _obj({
            "id": _STR, "user_id": _STR, "items": _array("OrderItem"),
            "status": _STR, "total": _NUM,
        }),
        "Notification": _obj({"id": _STR, "user_id": _STR, "message": _STR}),
        "NotificationInput": _obj({"message": _STR}, ["message"], {"message": "Hola, tu pedido va en camino"}),
        "Health": _obj({"status": _STR}),
    }

    paths = {
        "/health": {"get": _op("Sistema", "Estado de la API", _ref("Health"))},
        "/users": {
            "get": _op("Usuarios", "Listar usuarios", _array("User")),
            "post": _op("Usuarios", "Registrar usuario", _ref("User"), "201", "UserInput", errors=("400", "409")),
        },
        "/users/{user_id}": {
            "get": _op("Usuarios", "Obtener usuario", _ref("User"), params=("user_id",), errors=("404",)),
        },
        "/products": {
            "get": _op("Productos", "Listar productos", _array("Product")),
            "post": _op("Productos", "Crear producto", _ref("Product"), "201", "ProductInput", errors=("400",)),
        },
        "/products/{product_id}": {
            "get": _op("Productos", "Obtener producto", _ref("Product"), params=("product_id",), errors=("404",)),
        },
        "/inventory/{product_id}": {
            "get": _op("Inventario", "Consultar stock", _ref("StockItem"), params=("product_id",), errors=("404",)),
            "put": _op("Inventario", "Definir stock", _ref("StockItem"), body="StockInput",
                       params=("product_id",), errors=("400", "404")),
        },
        "/orders": {
            "get": _op("Pedidos", "Listar pedidos", _array("Order")),
            "post": _op("Pedidos", "Crear pedido (descuenta stock y notifica)", _ref("Order"), "201",
                        "OrderInput", errors=("400", "404", "409")),
        },
        "/orders/{order_id}": {
            "get": _op("Pedidos", "Obtener pedido", _ref("Order"), params=("order_id",), errors=("404",)),
        },
        "/notifications/{user_id}": {
            "get": _op("Notificaciones", "Listar notificaciones de un usuario", _array("Notification"),
                       params=("user_id",), errors=("404",)),
            "post": _op("Notificaciones", "Enviar notificación a un usuario", _ref("Notification"), "201",
                        "NotificationInput", params=("user_id",), errors=("400", "404")),
        },
    }

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Mercado hexagonal",
            "version": "1.0.0",
            "description": "API con 5 servicios (usuarios, productos, inventario, pedidos y "
                           "notificaciones) sobre arquitectura hexagonal.",
        },
        "tags": [{"name": n} for n in ("Usuarios", "Productos", "Inventario", "Pedidos", "Notificaciones", "Sistema")],
        "paths": paths,
        "components": {"schemas": schemas},
    }
