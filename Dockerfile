# syntax=docker/dockerfile:1
# Stage de construccion: instala las dependencias y prepara la aplicacion.
# Se usa una imagen separada para no incluir herramientas de instalacion en runtime.
FROM python:3.13-slim AS build

# Copia uv desde su imagen oficial para gestionar el entorno y las dependencias.
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

WORKDIR /app

# Genera bytecode durante la instalacion y copia paquetes al entorno virtual
# en lugar de enlazarlos, para que el entorno pueda copiarse entre stages.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Se copian primero los manifiestos para aprovechar la cache si solo cambia el codigo.
COPY uv.lock pyproject.toml ./

# El cache acelera instalaciones posteriores. --frozen respeta uv.lock;
# --no-install-project deja la instalacion del proyecto para despues de copiar el codigo.
# --no-dev omite dependencias de desarrollo en la imagen.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copia la aplicacion luego de instalar dependencias para conservar la cache anterior.
COPY . .

# Instala ahora el proyecto, manteniendo las versiones fijadas en uv.lock.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Stage final: contiene solo la aplicacion preparada y la imagen minima de ejecucion.
FROM python:3.13-slim AS runtime

# Prioriza los ejecutables del entorno virtual creado en el stage build.
ENV PATH="/app/.venv/bin:$PATH"

# Crea un usuario sin privilegios de login para ejecutar el servicio con permisos limitados.
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -d /app -s /bin/false appuser

WORKDIR /app

# Copia el entorno virtual y el codigo, asignando su propiedad al usuario de runtime.
COPY --from=build --chown=appuser:appgroup /app .

# Evita ejecutar la aplicacion como root.
USER appuser

# Inicia FastAPI escuchando en todas las interfaces del contenedor, puerto 8000.
ENTRYPOINT ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
