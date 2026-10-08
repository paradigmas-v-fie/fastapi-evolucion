import uuid

from app.products.schemas import ProductoActualizar, ProductoCrear, ProductoDetalle


class ProductoNoEncontrado(Exception):
    def __init__(self, producto_id: str) -> None:
        self.producto_id = producto_id
        super().__init__("Producto no encontrado")


class Service:
    """Casos de uso del catálogo. En esta rama también guarda los datos."""

    def __init__(self) -> None:
        self._productos: list[dict] = []

    def listar(self) -> list[ProductoDetalle]:
        return [ProductoDetalle(**producto) for producto in self._productos]

    def crear(self, datos: ProductoCrear) -> ProductoDetalle:
        producto = {
            "id": str(uuid.uuid4()),
            "nombre": datos.nombre,
            "precio_base": datos.precio_base,
        }
        self._productos.append(producto)
        return ProductoDetalle(**producto)

    def obtener(self, producto_id: str) -> ProductoDetalle:
        return ProductoDetalle(**self._buscar(producto_id))

    def actualizar(self, producto_id: str, datos: ProductoActualizar) -> ProductoDetalle:
        producto = self._buscar(producto_id)
        producto["nombre"] = datos.nombre
        producto["precio_base"] = datos.precio_base
        return ProductoDetalle(**producto)

    def eliminar(self, producto_id: str) -> None:
        self._productos.remove(self._buscar(producto_id))

    def _buscar(self, producto_id: str) -> dict:
        for producto in self._productos:
            if producto["id"] == producto_id:
                return producto
        raise ProductoNoEncontrado(producto_id)
