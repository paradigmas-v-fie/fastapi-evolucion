from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_raiz_responde_hola():
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "Hola"}


def test_openapi_esta_publicado():
    respuesta = client.get("/openapi.json")

    assert respuesta.status_code == 200
    assert respuesta.json()["info"]["title"] == "Tienda"
