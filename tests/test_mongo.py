from app.products.domain import Producto
from app.products.mongo_repository import a_documento, desde_documento


def test_el_documento_conserva_identidad_y_precio():
    producto = Producto(nombre="Yerba", precio_base=100, producto_id="abc")

    recuperado = desde_documento(a_documento(producto))

    assert recuperado.id == "abc"
    assert recuperado.nombre == "Yerba"
    assert recuperado.precio_base == 100
    assert recuperado.precio_final() == 121.0
