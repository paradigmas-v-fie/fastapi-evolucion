# 01 — API mínima

Esta rama deja corriendo un proceso FastAPI con una sola ruta. No hay recursos,
dominio ni base de datos: el objetivo es ver el ciclo pedido-respuesta y el
contrato que publica OpenAPI.

## Cómo ejecutar

Hace falta [uv](https://docs.astral.sh/uv/) y Python 3.13. Si no tenés ese
Python, `uv` puede instalarlo.

```bash
uv python install 3.13
uv sync
uv run fastapi dev main.py
```

Dejá esa terminal abierta. La API queda en `http://127.0.0.1:8000`.

- `GET /` responde `{"mensaje": "Hola"}`.
- `http://127.0.0.1:8000/docs` muestra Swagger UI.
- `http://127.0.0.1:8000/openapi.json` es la descripción del contrato.

```bash
curl -i http://127.0.0.1:8000/
```

Para cortar el servidor, `Ctrl+C`.

## Qué mirar en el código

Todo está en [`main.py`](main.py): se crea la aplicación, se registra una ruta
y la función devuelve un diccionario. FastAPI lo serializa a JSON y genera la
documentación a partir de la firma.

## Verificar sin levantar el servidor

```bash
bash verificar.sh
```

## Siguiente rama

`02-recurso-rest` agrega el recurso `/productos` en este mismo archivo. Los
datos viven en memoria: reiniciar el proceso los borra.

```bash
git switch 02-recurso-rest
```
