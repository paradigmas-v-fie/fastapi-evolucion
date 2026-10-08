from fastapi import FastAPI

app = FastAPI(title="Tienda")


@app.get("/")
def raiz() -> dict[str, str]:
    return {"mensaje": "Hola"}
