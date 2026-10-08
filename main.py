import uuid

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Tienda")

# El catálogo vive en el proceso. Reiniciar el servidor borra los productos.
_productos: list[dict] = []


class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=1)
    precio_base: float = Field(gt=0)


class ProductoActualizar(BaseModel):
    nombre: str = Field(min_length=1)
    precio_base: float = Field(gt=0)


class ProductoDetalle(BaseModel):
    id: str
    nombre: str
    precio_base: float


@app.get("/")
def raiz() -> dict[str, str]:
    return {"mensaje": "Hola"}


@app.get("/productos")
def listar() -> list[ProductoDetalle]:
    return [ProductoDetalle(**producto) for producto in _productos]


@app.post("/productos", status_code=status.HTTP_201_CREATED)
def crear(datos: ProductoCrear) -> ProductoDetalle:
    producto = {
        "id": str(uuid.uuid4()),
        "nombre": datos.nombre,
        "precio_base": datos.precio_base,
    }
    _productos.append(producto)
    return ProductoDetalle(**producto)


@app.get("/productos/{producto_id}")
def obtener(producto_id: str) -> ProductoDetalle:
    producto = _buscar(producto_id)
    return ProductoDetalle(**producto)


@app.put("/productos/{producto_id}")
def actualizar(producto_id: str, datos: ProductoActualizar) -> ProductoDetalle:
    producto = _buscar(producto_id)
    producto["nombre"] = datos.nombre
    producto["precio_base"] = datos.precio_base
    return ProductoDetalle(**producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(producto_id: str) -> None:
    producto = _buscar(producto_id)
    _productos.remove(producto)


def _buscar(producto_id: str) -> dict:
    for producto in _productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
