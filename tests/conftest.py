import pytest
from fastapi.testclient import TestClient

from app.auth.dependencies import usuario_actual
from app.main import crear_aplicacion
from app.products.repository import RepositorioEnMemoria


def _admin() -> dict:
    return {"preferred_username": "admin", "realm_access": {"roles": ["admin"]}}


@pytest.fixture
def client():
    # El servidor usa Mongo y Keycloak. Acá el contrato HTTP se prueba en memoria
    # y el token de admin se reemplaza para no pedir uno real.
    aplicacion = crear_aplicacion(RepositorioEnMemoria())
    aplicacion.dependency_overrides[usuario_actual] = _admin
    with TestClient(aplicacion) as cliente:
        yield cliente
