import pytest
from fastapi.testclient import TestClient

from app.main import crear_aplicacion
from app.products.repository import RepositorioEnMemoria


@pytest.fixture
def client():
    # El servidor de esta rama usa Mongo. El contrato HTTP se prueba en memoria.
    aplicacion = crear_aplicacion(RepositorioEnMemoria())
    with TestClient(aplicacion) as cliente:
        yield cliente
