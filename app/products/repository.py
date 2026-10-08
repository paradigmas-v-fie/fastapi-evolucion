from typing import Protocol

from app.products.domain import Producto


class Repositorio(Protocol):
    def agregar(self, producto: Producto) -> None: ...

    def listar(self) -> list[Producto]: ...

    def obtener(self, producto_id: str) -> Producto | None: ...

    def eliminar(self, producto_id: str) -> bool: ...

    def actualizar(self, producto: Producto) -> None: ...


class RepositorioEnMemoria:
    """Guarda objetos en el proceso. Sirve para desarrollar sin una base."""

    def __init__(self) -> None:
        self._productos: dict[str, Producto] = {}

    def agregar(self, producto: Producto) -> None:
        self._productos[producto.id] = producto

    def listar(self) -> list[Producto]:
        return list(self._productos.values())

    def obtener(self, producto_id: str) -> Producto | None:
        return self._productos.get(producto_id)

    def eliminar(self, producto_id: str) -> bool:
        return self._productos.pop(producto_id, None) is not None

    def actualizar(self, producto: Producto) -> None:
        if producto.id not in self._productos:
            return
        self._productos[producto.id] = producto
