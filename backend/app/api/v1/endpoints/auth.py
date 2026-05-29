from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencias import obtener_usuario_actual
from app.core.database import obtener_sesion
from app.core.seguridad import crear_token_acceso, verificar_contrasena
from app.models.usuario import Usuario
from app.schemas.auth import CredencialesLogin, TokenRespuesta, UsuarioActual

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenRespuesta)
async def login(
    credenciales: CredencialesLogin,
    sesion: AsyncSession = Depends(obtener_sesion),
) -> TokenRespuesta:
    resultado = await sesion.execute(
        select(Usuario)
        .options(selectinload(Usuario.persona))
        .where(Usuario.email == credenciales.email, Usuario.activo == True)
    )
    usuario = resultado.scalar_one_or_none()

    if not usuario or not verificar_contrasena(credenciales.contrasena, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contrasena incorrectos",
        )

    usuario.last_login = datetime.utcnow()
    await sesion.commit()

    token = crear_token_acceso({
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol": usuario.rol,
        "nombre_completo": usuario.persona.nombre_completo,
    })
    return TokenRespuesta(access_token=token)


@router.get("/me", response_model=UsuarioActual)
def me(usuario: UsuarioActual = Depends(obtener_usuario_actual)) -> UsuarioActual:
    return usuario
