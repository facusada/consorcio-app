import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencias import obtener_usuario_actual
from app.core.database import obtener_sesion
from app.models.persona import Persona
from app.models.unidad_persona import UnidadPersona
from app.schemas.auth import UsuarioActual

router = APIRouter(prefix="/propietarios", tags=["propietarios"])


class PropietarioRespuesta:
    pass


from pydantic import BaseModel


class PropietarioSimple(BaseModel):
    id: uuid.UUID
    nombre: str
    apellido: str
    email: str | None

    model_config = {"from_attributes": True}


class UnidadDePropietario(BaseModel):
    id: uuid.UUID
    codigo: str
    tipo: str
    indice_prorrateo: float

    model_config = {"from_attributes": True}


class PropietarioDetalle(PropietarioSimple):
    unidades: list[UnidadDePropietario] = []


@router.get("", response_model=list[PropietarioSimple])
async def listar_propietarios(
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> list[PropietarioSimple]:
    resultado = await sesion.execute(
        select(Persona)
        .where(Persona.tipo == "propietario")
        .order_by(Persona.apellido, Persona.nombre)
    )
    personas = resultado.scalars().all()
    return [PropietarioSimple.model_validate(p) for p in personas]


@router.get("/{persona_id}", response_model=PropietarioDetalle)
async def detalle_propietario(
    persona_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> PropietarioDetalle:
    resultado = await sesion.execute(
        select(Persona)
        .options(
            selectinload(Persona.unidades)
            .selectinload(UnidadPersona.unidad)
        )
        .where(Persona.id == persona_id)
    )
    persona = resultado.scalar_one_or_none()
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado")

    unidades_vigentes = [
        UnidadDePropietario(
            id=up.unidad.id,
            codigo=up.unidad.codigo,
            tipo=up.unidad.tipo,
            indice_prorrateo=float(up.unidad.indice_prorrateo),
        )
        for up in persona.unidades
        if up.vigente and up.rol == "propietario"
    ]

    return PropietarioDetalle(
        id=persona.id,
        nombre=persona.nombre,
        apellido=persona.apellido,
        email=persona.email,
        unidades=unidades_vigentes,
    )
