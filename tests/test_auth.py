from fastapi.testclient import TestClient

from app.auth.dependencies import usuario_actual
from app.main import crear_aplicacion
from app.products.repository import RepositorioEnMemoria


def test_crear_sin_token_responde_401():
    aplicacion = crear_aplicacion(RepositorioEnMemoria())

    with TestClient(aplicacion) as cliente:
        respuesta = cliente.post(
            "/productos",
            json={"nombre": "Yerba", "precio_base": 1500},
        )

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Falta el token"


def test_listar_sigue_publico():
    aplicacion = crear_aplicacion(RepositorioEnMemoria())

    with TestClient(aplicacion) as cliente:
        respuesta = cliente.get("/productos")

    assert respuesta.status_code == 200


def test_un_usuario_sin_rol_admin_recibe_403():
    aplicacion = crear_aplicacion(RepositorioEnMemoria())
    aplicacion.dependency_overrides[usuario_actual] = lambda: {
        "preferred_username": "alumno",
        "realm_access": {"roles": ["user"]},
    }

    with TestClient(aplicacion) as cliente:
        respuesta = cliente.post(
            "/productos",
            json={"nombre": "Yerba", "precio_base": 1500},
        )

    assert respuesta.status_code == 403
    assert respuesta.json()["detail"] == "Se requiere el rol admin"
