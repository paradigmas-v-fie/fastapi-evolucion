def test_raiz_responde_hola(client):
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "Hola"}


def test_openapi_esta_publicado(client):
    respuesta = client.get("/openapi.json")

    assert respuesta.status_code == 200
    assert "/productos" in respuesta.json()["paths"]


def test_crear_listar_y_obtener(client):
    creado = client.post("/productos", json={"nombre": "Yerba", "precio_base": 1500})

    assert creado.status_code == 201
    cuerpo = creado.json()
    assert cuerpo["nombre"] == "Yerba"
    assert cuerpo["precio_base"] == 1500
    assert cuerpo["precio_final"] == 1815.0
    assert cuerpo["id"]

    listado = client.get("/productos")
    assert cuerpo["id"] in {item["id"] for item in listado.json()}

    obtenido = client.get(f"/productos/{cuerpo['id']}")
    assert obtenido.status_code == 200
    assert obtenido.json() == cuerpo


def test_actualizar_reemplaza_nombre_y_precio(client):
    creado = client.post("/productos", json={"nombre": "Yerba", "precio_base": 1500}).json()

    respuesta = client.put(
        f"/productos/{creado['id']}",
        json={"nombre": "Yerba suave", "precio_base": 2000},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == creado["id"]
    assert respuesta.json()["nombre"] == "Yerba suave"
    assert respuesta.json()["precio_base"] == 2000
    assert respuesta.json()["precio_final"] == 2420.0


def test_eliminar_despues_responde_404(client):
    creado = client.post("/productos", json={"nombre": "Yerba", "precio_base": 1500}).json()

    borrado = client.delete(f"/productos/{creado['id']}")

    assert borrado.status_code == 204
    assert borrado.content == b""
    assert client.get(f"/productos/{creado['id']}").status_code == 404


def test_obtener_inexistente_responde_404(client):
    respuesta = client.get("/productos/no-existe")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Producto no encontrado"


def test_precio_no_positivo_lo_rechaza_el_dominio(client):
    respuesta = client.post("/productos", json={"nombre": "Yerba", "precio_base": 0})

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El precio base tiene que ser mayor a cero"


def test_nombre_vacio_lo_rechaza_el_dominio(client):
    respuesta = client.post("/productos", json={"nombre": "   ", "precio_base": 1500})

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El nombre no puede estar vacío"


def test_falta_un_campo_responde_422(client):
    respuesta = client.post("/productos", json={"nombre": "Yerba"})

    assert respuesta.status_code == 422
