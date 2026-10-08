from pydantic import BaseModel

from app.products.domain import Producto


class ProductoCrear(BaseModel):
    nombre: str
    precio_base: float


class ProductoActualizar(BaseModel):
    nombre: str
    precio_base: float


class ProductoDetalle(BaseModel):
    id: str
    nombre: str
    precio_base: float
    precio_final: float

    @classmethod
    def desde_dominio(cls, producto: Producto) -> "ProductoDetalle":
        return cls(
            id=producto.id,
            nombre=producto.nombre,
            precio_base=producto.precio_base,
            precio_final=producto.precio_final(),
        )
