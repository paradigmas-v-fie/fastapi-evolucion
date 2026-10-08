# 07 — Compose

Un comando levanta la API y MongoDB. La aplicación que corre adentro del
contenedor es la misma de la rama anterior: cambia el ambiente, no las capas.

Dentro de la red de Compose la base se llama `db`. Por eso el servicio `api`
define `MONGO_HOST=db`. Si corrés la API en el host, el default sigue siendo
`localhost`, porque el puerto `27017` está publicado.

El contenedor usa `fastapi run`: sin recarga automática. Para programar con
recarga, levantá solo la base y seguí usando `fastapi dev`.

## Ambiente completo

```bash
docker compose up --build
```

La API queda en `http://127.0.0.1:8000`. Compose espera a que Mongo responda
antes de arrancar la API.

```bash
curl -s -X POST http://127.0.0.1:8000/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Yerba","precio_base":1500}'
```

`Ctrl+C` detiene los contenedores. `docker compose down` los elimina. El
volumen de Mongo se conserva; `docker compose down -v` lo borra.

## Durante la clase, con recarga

No hace falta el contenedor de la API:

```bash
docker compose up -d db
uv sync
uv run fastapi dev main.py
```

No corras los dos a la vez: los dos quieren el puerto `8000`.

## Qué cambió

```bash
git diff 06-mongodb..07-compose
```

Aparecen `Dockerfile` y el servicio `api` en `docker-compose.yaml`. El Python
de las capas no cambia.

## Verificar el código sin Docker

```bash
bash verificar.sh
```

Eso no construye la imagen. Para comprobar el ambiente completo, usá
`docker compose up --build` y el `curl` de arriba.

## Siguiente rama

`08-autenticacion` suma Keycloak al mismo Compose. Leer productos sigue
público; crear, reemplazar y borrar exigen el rol `admin`.

```bash
git switch 08-autenticacion
```
