import pytest

from app.products.domain import IVA, Producto, ProductoInvalido


def test_el_precio_final_aplica_iva():
    producto = Producto(nombre="Yerba", precio_base=1500, producto_id="abc")

    assert producto.id == "abc"
    assert producto.precio_final() == 1815.0


def test_iva_redondea_a_centavos():
    assert IVA().aplicar(10) == 12.1


def test_no_se_construye_con_precio_no_positivo():
    with pytest.raises(ProductoInvalido):
        Producto(nombre="Yerba", precio_base=0)


def test_actualizar_vuelve_a_validar():
    producto = Producto(nombre="Yerba", precio_base=1500)

    with pytest.raises(ProductoInvalido):
        producto.actualizar("   ", 1500)

    assert producto.nombre == "Yerba"
