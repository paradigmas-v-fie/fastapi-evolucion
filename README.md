# 08 — Autenticación

Leer el catálogo sigue siendo público. Crear, reemplazar y borrar exigen un
token del realm `tienda` con el rol `admin`. Keycloak entra al mismo Compose.
No hay que crear el realm a mano: se importa `keycloak/tienda-realm.json` al
arrancar.

| Usuario | Contraseña | Rol | Puede escribir |
| --- | --- | --- | --- |
| `admin` | `admin` | `admin` | sí |
| `alumno` | `alumno` | `user` | no |

Esas claves son del entorno local de la cursada. La consola de administración
de Keycloak, en el realm `master`, usa el usuario de arranque `admin` /
`admin` y no es el mismo usuario que escribe productos.

## Ambiente completo

```bash
docker compose up --build
```

Keycloak tarda más que la API. Esperá a que abra `http://127.0.0.1:8080` antes
de pedir un token. Hasta ese momento, una escritura responde `503`.

```bash
TOKEN=$(curl -s -X POST \
  http://127.0.0.1:8080/realms/tienda/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=tienda-api" \
  -d "grant_type=password" \
  -d "username=admin" \
  -d "password=admin" \
  | python -c "import json, sys; print(json.load(sys.stdin)['access_token'])")

curl -i http://127.0.0.1:8000/productos

curl -i -X POST http://127.0.0.1:8000/productos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Yerba","precio_base":1500}'
```

Sin encabezado, esa escritura responde `401`. Con el token de `alumno`,
responde `403`.

El token pedido a `localhost` dice que lo emitió `localhost`. La API, dentro
de Compose, busca las claves públicas en `http://keycloak:8080`. La validación
compara el realm (`/realms/tienda`), no el host. Está explicado en
`app/auth/keycloak.py`.

## Durante la clase, con recarga

```bash
docker compose up -d db keycloak
uv sync
uv run fastapi dev main.py
```

En el host no hace falta exportar `KEYCLOAK_URL`: el default ya es
`http://localhost:8080`. No levantes también el servicio `api` si vas a usar
el puerto `8000` en la máquina.

## Qué cambió

```bash
git diff 07-compose..08-autenticacion
```

- `app/auth/dependencies.py` exige el rol en las rutas que escriben.
- `GET /productos` y `GET /productos/{id}` no cambiaron.
- El service y el dominio no conocen a Keycloak.

## Verificar sin Docker ni Keycloak

```bash
bash verificar.sh
```

Eso cubre el `401`, el `403` y que el listado siga público. No pide un token
real.

## Fin del recorrido

Esta es la última capa. Para volver al mapa de ramas:

```bash
git switch main
```
