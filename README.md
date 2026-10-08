# 02 — Recurso REST

Esta rama expone `/productos` en el mismo `main.py` de la rama anterior. El
catálogo es una lista en memoria. Reiniciar el proceso vuelve a dejarla vacía.

El contrato HTTP que aparece acá se mantiene en las ramas siguientes. Lo que
cambia después es dónde viven las reglas y los datos, no los verbos.

## Cómo ejecutar

```bash
uv sync
uv run fastapi dev main.py
```

```bash
curl -i http://127.0.0.1:8000/productos

curl -i -X POST http://127.0.0.1:8000/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Yerba","precio_base":1500}'
```

El `id` lo asigna el servidor. Usalo para consultar, reemplazar o borrar:

| Operación | Resultado |
| --- | --- |
| `GET /productos` | `200` y la lista, vacía si todavía no hay productos |
| `POST /productos` | `201` y el producto creado |
| `GET /productos/{id}` | `200` y el producto; `404` si no existe |
| `PUT /productos/{id}` | `200` y el producto con nombre y precio reemplazados; `404` si no existe |
| `DELETE /productos/{id}` | `204` sin cuerpo; `404` si no existe |

Un precio menor o igual a cero, o un nombre vacío, responde `422`: esa
validación está en el modelo de Pydantic, al lado de la ruta. La rama
`04-dominio` mueve esa regla al objeto.

Swagger sigue en `http://127.0.0.1:8000/docs`.

## Qué cambió

```bash
git diff 01-api-minima..02-recurso-rest
```

Sigue habiendo un solo archivo de aplicación. La ruta, el DTO y la lista están
juntos. Eso alcanza para un recurso chico y se vuelve difícil de leer cuando
aparecen reglas de negocio.

## Verificar

```bash
bash verificar.sh
```

## Siguiente rama

`03-capas` separa router, service y schemas. El comando de ejecución no cambia
y el catálogo sigue en memoria.

```bash
git switch 03-capas
```
