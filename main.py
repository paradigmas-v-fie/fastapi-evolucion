"""Punto de entrada estable.

Las ramas siguientes cambian el interior de ``app/``. Este archivo queda para
que el comando no cambie:

    uv run fastapi dev main.py
"""

from app.main import app

__all__ = ["app"]
