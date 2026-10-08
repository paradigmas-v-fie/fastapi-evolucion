# 03 — Capas

El recurso `/productos` queda partido en tres lugares. El catálogo sigue en
memoria y el comando de ejecución no cambia.

| Archivo | Responsabilidad |
| --- | --- |
| `app/products/router.py` | HTTP: verbo, path, código de estado |
| `app/products/service.py` | Caso de uso y, por ahora, la lista |
| `app/products/schemas.py` | DTO de entrada y de salida |
| `app/main.py` | Arma la aplicación e incluye el router |
| `main.py` | Punto de entrada estable |

`Producto no encontrado` ya no se arma con `HTTPException` dentro del caso de
uso. El service lanza su propia excepción y `app/main.py` la traduce a `404`.
El service no importa FastAPI.

## Cómo ejecutar

```bash
uv sync
uv run fastapi dev main.py
```

Las mismas peticiones de la rama anterior siguen valiendo. Un `POST` con precio
`0` sigue respondiendo `422`, porque la regla todavía está en el schema.

## Qué cambió

```bash
git diff 02-recurso-rest..03-capas
```

El contrato HTTP no cambia. Cambia quién conoce la lista.

## Verificar

```bash
bash verificar.sh
```

## Siguiente rama

`04-dominio` saca las reglas del schema y las pone en un `Producto`. El precio
final con IVA aparece en la respuesta.

```bash
git switch 04-dominio
```
