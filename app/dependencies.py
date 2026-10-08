from app.products.service import Service

# Lo completa el arranque de la aplicación. Importar el módulo no conecta a Mongo.
servicio_actual: Service | None = None


def obtener_servicio() -> Service:
    if servicio_actual is None:
        raise RuntimeError("La aplicación todavía no tiene un repositorio")
    return servicio_actual
