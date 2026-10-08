import uuid


class ProductoInvalido(ValueError):
    """La operación dejaría un producto que no cumple sus invariantes."""


class IVA:
    PORCENTAJE = 0.21

    def aplicar(self, precio: float) -> float:
        return round(precio * (1 + self.PORCENTAJE), 2)


class Producto:
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        producto_id: str | None = None,
    ) -> None:
        self.id = producto_id or str(uuid.uuid4())
        self.nombre = _nombre_valido(nombre)
        self.precio_base = _precio_valido(precio_base)
        self._iva = IVA()

    def precio_final(self) -> float:
        return self._iva.aplicar(self.precio_base)

    def actualizar(self, nombre: str, precio_base: float) -> None:
        self.nombre = _nombre_valido(nombre)
        self.precio_base = _precio_valido(precio_base)


def _nombre_valido(nombre: str) -> str:
    nombre_limpio = nombre.strip()
    if not nombre_limpio:
        raise ProductoInvalido("El nombre no puede estar vacío")
    return nombre_limpio


def _precio_valido(precio_base: float) -> float:
    if precio_base <= 0:
        raise ProductoInvalido("El precio base tiene que ser mayor a cero")
    return precio_base
