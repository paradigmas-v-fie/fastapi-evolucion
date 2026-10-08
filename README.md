# 04 — Dominio

El catálogo deja de guardar diccionarios. El service construye un `Producto` y
el schema solo transporta datos. El IVA no se calcula en la ruta.

La respuesta ahora incluye `precio_final`. Para una yerba de `1500`, el precio
final es `1815`: el 21 % vive en `IVA`, dentro del dominio.

Un precio no positivo o un nombre vacío responde `400`. Antes respondía `422`,
porque la regla estaba en Pydantic. Un JSON al que le falta un campo sigue
respondiendo `422`: eso es forma del mensaje, no una regla del producto.

## Cómo ejecutar

```bash
uv sync
uv run fastapi dev main.py
```

```bash
curl -s -X POST http://127.0.0.1:8000/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Yerba","precio_base":1500}'
```

## Qué cambió

```bash
git diff 03-capas..04-dominio
```

- `app/products/domain.py` protege nombre y precio, y calcula `precio_final`.
- `ProductoDetalle.desde_dominio` es el único cruce entre el objeto y el JSON.
- `app/main.py` traduce `ProductoInvalido` a `400`. El dominio no importa FastAPI.

En H1 el precio se componía con más modificadores. Acá el API siempre aplica
IVA para que el borde se pueda leer. Agregar otra variante es cambiar
`Producto.precio_final`, no el router.

## Verificar

```bash
bash verificar.sh
```

## Siguiente rama

`05-repositorio` le saca la lista al service. El caso de uso pide un
repositorio; la implementación de esta etapa sigue siendo memoria.

```bash
git switch 05-repositorio
```
