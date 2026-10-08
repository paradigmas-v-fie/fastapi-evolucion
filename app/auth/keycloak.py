import jwt
from jwt import PyJWKClient

from app.config import configuracion


class VerificadorKeycloak:
    """Valida la firma contra el JWKS de Keycloak.

    El emisor del token usa el host desde el que el alumno pidió el token
    (normalmente localhost). La API, si corre en Compose, busca las claves en
    el nombre interno ``keycloak``. Por eso se compara el realm, no el host.
    """

    def __init__(self) -> None:
        self._jwks: PyJWKClient | None = None

    def verificar(self, token: str) -> dict:
        clave = self._cliente_jwks().get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            clave.key,
            algorithms=["RS256"],
            options={"verify_aud": False, "verify_iss": False},
        )
        emisor = str(payload.get("iss", ""))
        if not emisor.endswith(f"/realms/{configuracion.keycloak_realm}"):
            raise jwt.InvalidTokenError("El token no pertenece al realm esperado")
        return payload

    def _cliente_jwks(self) -> PyJWKClient:
        if self._jwks is None:
            base = configuracion.keycloak_url.rstrip("/")
            url = f"{base}/realms/{configuracion.keycloak_realm}/protocol/openid-connect/certs"
            self._jwks = PyJWKClient(url)
        return self._jwks


verificador = VerificadorKeycloak()
