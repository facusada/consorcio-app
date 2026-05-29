import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencias import obtener_usuario_actual
from app.core.database import obtener_sesion
from app.models.unidad import UnidadFuncional
from app.models.unidad_persona import UnidadPersona
from app.schemas.auth import UsuarioActual
from app.schemas.unidad import UnidadDetalle, UnidadRespuesta

router = APIRouter(prefix="/unidades", tags=["unidades"])


@router.get("", response_model=list[UnidadRespuesta])
async def listar_unidades(
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> list[UnidadRespuesta]:
    resultado = await sesion.execute(
        select(UnidadFuncional).order_by(UnidadFuncional.tipo, UnidadFuncional.numero)
    )
    unidades = resultado.scalars().all()
    return [
        UnidadRespuesta(
            id=u.id,
            tipo=u.tipo,
            numero=u.numero,
            piso=u.piso,
            indice_prorrateo=u.indice_prorrateo,
            activa=u.activa,
            codigo=u.codigo,
        )
        for u in unidades
    ]


@router.get("/{unidad_id}", response_model=UnidadDetalle)
async def detalle_unidad(
    unidad_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> UnidadDetalle:
    resultado = await sesion.execute(
        select(UnidadFuncional)
        .options(
            selectinload(UnidadFuncional.personas).selectinload(UnidadPersona.persona)
        )
        .where(UnidadFuncional.id == unidad_id)
    )
    unidad = resultado.scalar_one_or_none()
    if not unidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")

    propietario = next(
        (up.persona for up in unidad.personas if up.rol == "propietario" and up.vigente),
        None,
    )
    return UnidadDetalle(
        id=unidad.id,
        tipo=unidad.tipo,
        numero=unidad.numero,
        piso=unidad.piso,
        indice_prorrateo=unidad.indice_prorrateo,
        activa=unidad.activa,
        codigo=unidad.codigo,
        propietario_nombre=propietario.nombre_completo if propietario else None,
    )
