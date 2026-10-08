# 05 — Repositorio

El service ya no tiene la lista. Recibe un repositorio y le pide agregar,
listar, obtener, actualizar y eliminar. La implementación de esta rama sigue
siendo memoria: se puede correr sin Docker y se puede leer el contrato antes
de ver MongoDB.

```text
main  →  Router  →  Service  →  RepositorioEnMemoria  →  Producto
```

El router no se entera del cambio. Sigue llamando a `service.crear` y
`service.listar`.

## Cómo ejecutar

```bash
uv sync
uv run fastapi dev main.py
```

El contrato HTTP es el de la rama anterior, incluido `precio_final`. Reiniciar
el proceso sigue borrando el catálogo: la memoria no resuelve la persistencia,
solo separa la responsabilidad.

## Qué cambió

```bash
git diff 04-dominio..05-repositorio
```

- `Repositorio` declara las operaciones. No es una clase de la que se hereda:
  `RepositorioEnMemoria` cumple el contrato por tener esos métodos.
- `Service` depende de ese contrato, no de un diccionario propio.
- `app/main.py` es quien elige la implementación. Cambiar de memoria a Mongo
  es cambiar esa elección, no las rutas.

## Verificar

```bash
bash verificar.sh
```

## Siguiente rama

`06-mongodb` agrega `RepositorioMongo`. Para correrla hace falta levantar la
base con Docker Compose; la API sigue arrancando con `uv run fastapi dev main.py`.

```bash
git switch 06-mongodb
```
