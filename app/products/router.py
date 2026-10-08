from fastapi import APIRouter, status

from app.products.schemas import ProductoActualizar, ProductoCrear, ProductoDetalle
from app.products.service import Service


class Router:
    """Traduce HTTP a llamadas del service. No guarda productos."""

    def __init__(self, servicio: Service) -> None:
        self._servicio = servicio
        self.router = APIRouter(prefix="/productos", tags=["productos"])
        self.router.add_api_route("", self.listar, methods=["GET"])
        self.router.add_api_route(
            "",
            self.crear,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route("/{producto_id}", self.obtener, methods=["GET"])
        self.router.add_api_route("/{producto_id}", self.actualizar, methods=["PUT"])
        self.router.add_api_route(
            "/{producto_id}",
            self.eliminar,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

    def listar(self) -> list[ProductoDetalle]:
        return self._servicio.listar()

    def crear(self, datos: ProductoCrear) -> ProductoDetalle:
        return self._servicio.crear(datos)

    def obtener(self, producto_id: str) -> ProductoDetalle:
        return self._servicio.obtener(producto_id)

    def actualizar(self, producto_id: str, datos: ProductoActualizar) -> ProductoDetalle:
        return self._servicio.actualizar(producto_id, datos)

    def eliminar(self, producto_id: str) -> None:
        self._servicio.eliminar(producto_id)
