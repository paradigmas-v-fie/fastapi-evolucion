from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.products.domain import ProductoInvalido
from app.products.router import Router
from app.products.service import ProductoNoEncontrado, Service


def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(title="Tienda")
    aplicacion.include_router(Router(Service()).router)
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
