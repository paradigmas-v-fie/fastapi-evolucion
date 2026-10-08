from app.products.domain import Producto
from app.products.schemas import ProductoActualizar, ProductoCrear, ProductoDetalle


class ProductoNoEncontrado(Exception):
    def __init__(self, producto_id: str) -> None:
        self.producto_id = producto_id
        super().__init__("Producto no encontrado")


class Service:
    """Casos de uso. Traduce DTOs a Producto y, por ahora, guarda la lista."""

    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def listar(self) -> list[ProductoDetalle]:
        return [ProductoDetalle.desde_dominio(producto) for producto in self._productos]

    def crear(self, datos: ProductoCrear) -> ProductoDetalle:
        producto = Producto(nombre=datos.nombre, precio_base=datos.precio_base)
        self._productos.append(producto)
        return ProductoDetalle.desde_dominio(producto)

    def obtener(self, producto_id: str) -> ProductoDetalle:
        return ProductoDetalle.desde_dominio(self._buscar(producto_id))

    def actualizar(self, producto_id: str, datos: ProductoActualizar) -> ProductoDetalle:
        producto = self._buscar(producto_id)
        producto.actualizar(datos.nombre, datos.precio_base)
        return ProductoDetalle.desde_dominio(producto)

    def eliminar(self, producto_id: str) -> None:
        self._productos.remove(self._buscar(producto_id))

    def _buscar(self, producto_id: str) -> Producto:
        for producto in self._productos:
            if producto.id == producto_id:
                return producto
        raise ProductoNoEncontrado(producto_id)
