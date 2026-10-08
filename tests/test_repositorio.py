from app.products.domain import Producto
from app.products.repository import RepositorioEnMemoria
from app.products.schemas import ProductoCrear
from app.products.service import Service


def test_dos_services_comparten_el_repositorio():
    repositorio = RepositorioEnMemoria()
    alta = Service(repositorio)
    consulta = Service(repositorio)

    creado = alta.crear(ProductoCrear(nombre="Yerba", precio_base=100))

    assert consulta.obtener(creado.id).nombre == "Yerba"


def test_eliminar_inexistente_informa_que_no_estaba():
    repositorio = RepositorioEnMemoria()

    assert repositorio.eliminar("no-existe") is False


def test_actualizar_guarda_el_objeto_modificado():
    repositorio = RepositorioEnMemoria()
    producto = Producto(nombre="Yerba", precio_base=100, producto_id="abc")
    repositorio.agregar(producto)

    producto.actualizar("Yerba suave", 200)
    repositorio.actualizar(producto)

    guardado = repositorio.obtener("abc")
    assert guardado is not None
    assert guardado.nombre == "Yerba suave"
    assert guardado.precio_base == 200
