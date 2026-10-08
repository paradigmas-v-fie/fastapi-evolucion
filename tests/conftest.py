import pytest
from fastapi.testclient import TestClient

from app.main import crear_aplicacion


@pytest.fixture
def client():
    return TestClient(crear_aplicacion())
