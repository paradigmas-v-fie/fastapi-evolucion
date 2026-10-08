from fastapi import APIRouter, Depends, status

from app.dependencies import obtener_servicio
from app.products.schemas import ProductoActualizar, ProductoCrear, ProductoDetalle
from app.products.service import Service


class Router:
    """Traduce HTTP a llamadas del service. El service llega en cada pedido."""

    def __init__(self) -> None:
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

    def listar(self, servicio: Service = Depends(obtener_servicio)) -> list[ProductoDetalle]:
        return servicio.listar()

    def crear(
        self,
        datos: ProductoCrear,
        servicio: Service = Depends(obtener_servicio),
    ) -> ProductoDetalle:
        return servicio.crear(datos)

    def obtener(
        self,
        producto_id: str,
        servicio: Service = Depends(obtener_servicio),
    ) -> ProductoDetalle:
        return servicio.obtener(producto_id)

    def actualizar(
        self,
        producto_id: str,
        datos: ProductoActualizar,
        servicio: Service = Depends(obtener_servicio),
    ) -> ProductoDetalle:
        return servicio.actualizar(producto_id, datos)

    def eliminar(
        self,
        producto_id: str,
        servicio: Service = Depends(obtener_servicio),
    ) -> None:
        servicio.eliminar(producto_id)
