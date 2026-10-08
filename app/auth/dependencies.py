from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError, PyJWKClientError

from app.auth.keycloak import verificador

_bearer = HTTPBearer(auto_error=False)


def usuario_actual(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return verificador.verificar(credentials.credentials)
    except InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    except PyJWKClientError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo validar el token contra Keycloak",
        ) from error


def requiere_rol(rol: str):
    def verificar(usuario: dict = Depends(usuario_actual)) -> dict:
        roles = usuario.get("realm_access", {}).get("roles", [])
        if rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere el rol {rol}",
            )
        return usuario

    return verificar
