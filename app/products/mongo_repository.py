from pymongo.database import Database

from app.products.domain import Producto


def a_documento(producto: Producto) -> dict:
    return {
        "producto_id": producto.id,
        "nombre": producto.nombre,
        "precio_base": producto.precio_base,
    }


def desde_documento(documento: dict) -> Producto:
    return Producto(
        nombre=documento["nombre"],
        precio_base=documento["precio_base"],
        producto_id=documento["producto_id"],
    )


class RepositorioMongo:
    def __init__(self, base: Database) -> None:
        self._coleccion = base["productos"]

    def agregar(self, producto: Producto) -> None:
        self._coleccion.insert_one(a_documento(producto))

    def listar(self) -> list[Producto]:
        return [desde_documento(documento) for documento in self._coleccion.find()]

    def obtener(self, producto_id: str) -> Producto | None:
        documento = self._coleccion.find_one({"producto_id": producto_id})
        if documento is None:
            return None
        return desde_documento(documento)

    def eliminar(self, producto_id: str) -> bool:
        resultado = self._coleccion.delete_one({"producto_id": producto_id})
        return resultado.deleted_count > 0

    def actualizar(self, producto: Producto) -> None:
        self._coleccion.update_one(
            {"producto_id": producto.id},
            {"$set": a_documento(producto)},
        )
