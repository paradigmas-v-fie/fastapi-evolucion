from pydantic import BaseModel, Field


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
