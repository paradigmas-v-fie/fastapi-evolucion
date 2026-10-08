from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.dependencies as dependencies
from app.internal.database import ConexionMongo
from app.products.domain import ProductoInvalido
from app.products.mongo_repository import RepositorioMongo
from app.products.repository import Repositorio
from app.products.router import Router
from app.products.service import ProductoNoEncontrado, Service

conexion = ConexionMongo()


def crear_aplicacion(repositorio: Repositorio | None = None) -> FastAPI:
    """Si no recibe repositorio, al arrancar conecta con MongoDB."""

    @asynccontextmanager
    async def lifespan(_aplicacion: FastAPI):
        if repositorio is not None:
            dependencies.servicio_actual = Service(repositorio)
            try:
                yield
            finally:
                dependencies.servicio_actual = None
            return

        base = conexion.conectar()
        dependencies.servicio_actual = Service(RepositorioMongo(base))
        try:
            yield
        finally:
            conexion.cerrar()
            dependencies.servicio_actual = None

    aplicacion = FastAPI(title="Tienda", lifespan=lifespan)
    aplicacion.include_router(Router().router)
    aplicacion.add_api_route("/", raiz, methods=["GET"])
    aplicacion.add_exception_handler(ProductoNoEncontrado, producto_no_encontrado)
    aplicacion.add_exception_handler(ProductoInvalido, producto_invalido)
    return aplicacion


def raiz() -> dict[str, str]:
    return {"mensaje": "Hola"}


def producto_no_encontrado(_request: Request, _error: ProductoNoEncontrado) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Producto no encontrado"})


def producto_invalido(_request: Request, error: ProductoInvalido) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(error)})


app = crear_aplicacion()
