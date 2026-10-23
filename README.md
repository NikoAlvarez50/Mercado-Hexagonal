# Mercado-Hexagonal (Flask)

Aplicación en Python + Flask con **arquitectura hexagonal** (puertos y adaptadores) y **5 servicios**:

| Servicio | Responsabilidad | Endpoints |
|---|---|---|
| Usuarios | Registro y consulta | `POST/GET /users`, `GET /users/<id>` |
| Productos | Catálogo | `POST/GET /products`, `GET /products/<id>` |
| Inventario | Existencias | `PUT/GET /inventory/<product_id>` |
| Pedidos | Orquesta los demás servicios | `POST/GET /orders`, `GET /orders/<id>` |
| Notificaciones | Aviso al usuario | `POST/GET /notifications/<user_id>` |

## Interfaz web y Swagger

Con el servidor corriendo (`python run.py`):

- `http://127.0.0.1:5000/` → interfaz web con una pestaña por servicio (formularios y tablas).
- `http://127.0.0.1:5000/docs` → Swagger UI para probar cada endpoint con "Try it out"
  (carga Swagger desde un CDN, requiere internet).
- `http://127.0.0.1:5000/openapi.json` → especificación OpenAPI.

Orden sugerido para probar: crear usuario → crear producto → definir stock → crear pedido → ver notificaciones.

## Análisis estático

```bash
pip install -r requirements-dev.txt
python scripts/check.py        # corre todo y muestra un resumen
```

| Chequeo | Herramienta | Qué garantiza |
|---|---|---|
| Aislamiento | import-linter | `infrastructure → application → domain` (nunca al revés); dominio y aplicación sin Flask; los 5 servicios no se importan entre sí; adaptadores de entrada y salida no se conocen; la entrada usa puertos, no servicios concretos |
| Código inseguro | Bandit | patrones comunes de riesgo de seguridad en `app/` y `run.py` |
| Código sin usar | ruff (`F`, `ARG`, `ERA`) | imports, variables y argumentos sin usar; código comentado |
| Código muerto | vulture | funciones, clases y atributos que nadie llama |
| Duplicación | pylint (`R0801`) | bloques repetidos entre archivos |

La configuración está en `pyproject.toml`. Cada herramienta también se puede ejecutar por separado:
`lint-imports`, `ruff check .`, `vulture`, `pylint --disable=all --enable=duplicate-code app`.

## Estructura

```
app/
├── domain/                       # Núcleo: entidades y excepciones (sin dependencias)
├── application/
│   ├── ports/
│   │   ├── inbound.py            # Puertos de entrada (casos de uso de cada servicio)
│   │   └── outbound.py           # Puertos de salida (repositorios, sender, ids)
│   └── services/                 # Los 5 servicios (implementan los puertos de entrada)
├── infrastructure/
│   ├── adapters/
│   │   ├── inbound/http/         # Adaptador Flask (blueprints de la API JSON)
│   │   ├── inbound/web/          # Adaptador web: interfaz HTML (/) y Swagger (/docs)
│   │   └── outbound/
│   │       ├── repositories/     # Un archivo por repositorio (en memoria) + base compartida
│   │       └── misc_adapters.py  # Generador de IDs y notificación por log
│   └── container.py              # Raíz de composición (inyección de dependencias)
└── main.py                       # create_app()
```

Regla de dependencias: `infrastructure → application → domain`. El dominio y los servicios
no importan Flask ni ningún adaptador; para cambiar la persistencia basta con crear un nuevo
adaptador de salida y cambiarlo en `container.py`.

## Ejecutar

```bash
pip install -r requirements.txt
python run.py            # http://localhost:5000
pytest                   # pruebas
```

## Ejemplo

```bash
curl -X POST localhost:5000/users -H 'Content-Type: application/json' -d '{"name":"Ana","email":"ana@mail.com"}'
curl -X POST localhost:5000/products -H 'Content-Type: application/json' -d '{"name":"Café","price":12.5}'
curl -X PUT  localhost:5000/inventory/<product_id> -H 'Content-Type: application/json' -d '{"quantity":10}'
curl -X POST localhost:5000/orders -H 'Content-Type: application/json' \
  -d '{"user_id":"<user_id>","items":[{"product_id":"<product_id>","quantity":2}]}'
```

Nota: la persistencia es en memoria (se pierde al reiniciar), pensada como adaptador de ejemplo.
