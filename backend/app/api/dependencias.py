from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.seguridad import decodificar_token
from app.schemas.auth import UsuarioActual

esquema_bearer = HTTPBearer()


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(esquema_bearer),
) -> UsuarioActual:
    token = credenciales.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
        )
    return UsuarioActual(
        id=payload.get("sub"),
        email=payload.get("email"),
        rol=payload.get("rol"),
        nombre_completo=payload.get("nombre_completo", ""),
    )


def solo_admin(usuario: UsuarioActual = Depends(obtener_usuario_actual)) -> UsuarioActual:
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido al administrador",
        )
    return usuario
