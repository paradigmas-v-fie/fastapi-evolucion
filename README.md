# 06 — MongoDB

El catálogo sobrevive al reinicio del proceso. `RepositorioMongo` cumple el
mismo contrato que `RepositorioEnMemoria`. La API sigue corriendo en la
máquina; Compose solo levanta la base.

La conexión no se abre al importar el módulo. Se abre en el arranque
(`lifespan`) y cada pedido recibe el service ya conectado mediante `Depends`.
Así un test puede usar memoria sin tener Docker, y el servidor no falla en el
import si la base todavía no está.

## Cómo ejecutar

Hace falta Docker.

```bash
uv sync
docker compose up -d
uv run fastapi dev main.py
```

Esperá a que el contenedor esté sano (`docker compose ps`) antes de crear
productos. Si la API arranca y Mongo no responde, el proceso termina con un
mensaje de conexión en vez de quedar a medias.

Los valores por defecto alcanzan para este Compose. Si querés dejarlos
escritos:

```bash
cp .env.example .env
```

Para inspeccionar los documentos, MongoDB Compass usa:

```text
mongodb://root:example@localhost:27017
```

La base se llama `tienda` y la colección, `productos`. Esas credenciales son
solo para el entorno local de la cursada.

```bash
curl -s -X POST http://127.0.0.1:8000/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Yerba","precio_base":1500}'
```

Reiniciá la API y volvé a listar: el producto sigue ahí. `docker compose down`
no borra el volumen. `docker compose down -v` sí.

## Qué cambió

```bash
git diff 05-repositorio..06-mongodb
```

- `app/products/mongo_repository.py` traduce `Producto` a un documento y al revés.
- `app/config.py` lee `MONGO_*`. Dentro de Compose, más adelante, `MONGO_HOST`
  va a ser `db` y no `localhost`.
- `app/main.py` elige `RepositorioMongo` al arrancar. Las rutas no se enteran.

## Verificar sin Docker

```bash
bash verificar.sh
```

Eso no prueba la conexión real. Prueba el mapeo del documento y que el
contrato HTTP sigue igual contra el repositorio en memoria.

## Siguiente rama

`07-compose` mete también la API en Compose. Un comando levanta el ambiente.

```bash
git switch 07-compose
```
