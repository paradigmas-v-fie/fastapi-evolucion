from app.products.domain import Producto
from app.products.repository import Repositorio
from app.products.schemas import ProductoActualizar, ProductoCrear, ProductoDetalle


class ProductoNoEncontrado(Exception):
    def __init__(self, producto_id: str) -> None:
        self.producto_id = producto_id
        super().__init__("Producto no encontrado")


class Service:
    """Casos de uso. No sabe si los productos están en memoria o en otra parte."""

    def __init__(self, repositorio: Repositorio) -> None:
        self._repositorio = repositorio

    def listar(self) -> list[ProductoDetalle]:
        return [
            ProductoDetalle.desde_dominio(producto) for producto in self._repositorio.listar()
        ]

    def crear(self, datos: ProductoCrear) -> ProductoDetalle:
        producto = Producto(nombre=datos.nombre, precio_base=datos.precio_base)
        self._repositorio.agregar(producto)
        return ProductoDetalle.desde_dominio(producto)

    def obtener(self, producto_id: str) -> ProductoDetalle:
        return ProductoDetalle.desde_dominio(self._exigir(producto_id))

    def actualizar(self, producto_id: str, datos: ProductoActualizar) -> ProductoDetalle:
        producto = self._exigir(producto_id)
        producto.actualizar(datos.nombre, datos.precio_base)
        self._repositorio.actualizar(producto)
        return ProductoDetalle.desde_dominio(producto)

    def eliminar(self, producto_id: str) -> None:
        if not self._repositorio.eliminar(producto_id):
            raise ProductoNoEncontrado(producto_id)

    def _exigir(self, producto_id: str) -> Producto:
        producto = self._repositorio.obtener(producto_id)
        if producto is None:
            raise ProductoNoEncontrado(producto_id)
        return producto
