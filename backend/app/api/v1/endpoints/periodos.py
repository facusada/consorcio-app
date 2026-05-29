import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencias import obtener_usuario_actual, solo_admin
from app.core.database import obtener_sesion
from app.models.detalle_expensa import DetalleExpensa
from app.models.gasto import Gasto
from app.models.liquidacion import Liquidacion
from app.models.periodo import Periodo
from app.models.unidad import UnidadFuncional
from app.models.unidad_persona import UnidadPersona
from app.schemas.auth import UsuarioActual
from app.schemas.gasto import GastoActualizar, GastoCrear, GastoRespuesta
from app.schemas.liquidacion import DetalleExpensaRespuesta, LiquidacionRespuesta
from app.schemas.periodo import CambioEstado, PeriodoCrear, PeriodoRespuesta
from app.services.calculo_expensas import DatosUnidad, calcular_expensas
from app.services.generador_pdf import generar_pdf_liquidacion

router = APIRouter(prefix="/periodos", tags=["periodos"])

CONSORCIO_ID_DEFAULT = None  # Se resuelve del usuario autenticado en futuras versiones


async def _obtener_consorcio_id(sesion: AsyncSession) -> uuid.UUID:
    from app.models.consorcio import Consorcio
    resultado = await sesion.execute(select(Consorcio).limit(1))
    consorcio = resultado.scalar_one_or_none()
    if not consorcio:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No existe consorcio configurado",
        )
    return consorcio.id


@router.get("", response_model=list[PeriodoRespuesta])
async def listar_periodos(
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> list[PeriodoRespuesta]:
    resultado = await sesion.execute(
        select(Periodo).order_by(Periodo.anio.desc(), Periodo.mes.desc())
    )
    periodos = resultado.scalars().all()
    return [
        PeriodoRespuesta(
            id=p.id, mes=p.mes, anio=p.anio, estado=p.estado,
            etiqueta=p.etiqueta, fecha_cierre=p.fecha_cierre,
        )
        for p in periodos
    ]


@router.post("", response_model=PeriodoRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_periodo(
    datos: PeriodoCrear,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(solo_admin),
) -> PeriodoRespuesta:
    consorcio_id = await _obtener_consorcio_id(sesion)

    existente = await sesion.execute(
        select(Periodo).where(
            Periodo.consorcio_id == consorcio_id,
            Periodo.mes == datos.mes,
            Periodo.anio == datos.anio,
        )
    )
    if existente.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un periodo para {datos.mes}/{datos.anio}",
        )

    periodo = Periodo(consorcio_id=consorcio_id, mes=datos.mes, anio=datos.anio)
    sesion.add(periodo)
    await sesion.commit()
    await sesion.refresh(periodo)
    return PeriodoRespuesta(
        id=periodo.id, mes=periodo.mes, anio=periodo.anio, estado=periodo.estado,
        etiqueta=periodo.etiqueta, fecha_cierre=periodo.fecha_cierre,
    )


@router.get("/{periodo_id}", response_model=PeriodoRespuesta)
async def detalle_periodo(
    periodo_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> PeriodoRespuesta:
    periodo = await sesion.get(Periodo, periodo_id)
    if not periodo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Periodo no encontrado")
    return PeriodoRespuesta(
        id=periodo.id, mes=periodo.mes, anio=periodo.anio, estado=periodo.estado,
        etiqueta=periodo.etiqueta, fecha_cierre=periodo.fecha_cierre,
    )


@router.patch("/{periodo_id}/estado", response_model=PeriodoRespuesta)
async def cambiar_estado(
    periodo_id: uuid.UUID,
    datos: CambioEstado,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(solo_admin),
) -> PeriodoRespuesta:
    periodo = await sesion.get(Periodo, periodo_id)
    if not periodo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Periodo no encontrado")

    _validar_transicion_estado(periodo.estado, datos.estado)

    if datos.estado == "cerrado":
        periodo.fecha_cierre = date.today()
    periodo.estado = datos.estado
    await sesion.commit()
    await sesion.refresh(periodo)
    return PeriodoRespuesta(
        id=periodo.id, mes=periodo.mes, anio=periodo.anio, estado=periodo.estado,
        etiqueta=periodo.etiqueta, fecha_cierre=periodo.fecha_cierre,
    )


def _validar_transicion_estado(actual: str, nuevo: str) -> None:
    transiciones_validas = {
        "abierto": {"liquidado"},
        "liquidado": {"abierto", "cerrado"},
        "cerrado": set(),
    }
    if nuevo not in transiciones_validas.get(actual, set()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Transicion invalida: {actual} -> {nuevo}",
        )


@router.get("/{periodo_id}/gastos", response_model=list[GastoRespuesta])
async def listar_gastos(
    periodo_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> list[GastoRespuesta]:
    resultado = await sesion.execute(
        select(Gasto).where(Gasto.periodo_id == periodo_id).order_by(Gasto.fecha)
    )
    gastos = resultado.scalars().all()
    return [GastoRespuesta.model_validate(g) for g in gastos]


@router.post("/{periodo_id}/gastos", response_model=GastoRespuesta, status_code=status.HTTP_201_CREATED)
async def agregar_gasto(
    periodo_id: uuid.UUID,
    datos: GastoCrear,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(solo_admin),
) -> GastoRespuesta:
    periodo = await sesion.get(Periodo, periodo_id)
    if not periodo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Periodo no encontrado")
    if periodo.estado != "abierto":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Solo se pueden agregar gastos en periodos abiertos",
        )

    gasto = Gasto(periodo_id=periodo_id, **datos.model_dump())
    sesion.add(gasto)
    await sesion.commit()
    await sesion.refresh(gasto)
    return GastoRespuesta.model_validate(gasto)


@router.put("/{periodo_id}/gastos/{gasto_id}", response_model=GastoRespuesta)
async def editar_gasto(
    periodo_id: uuid.UUID,
    gasto_id: uuid.UUID,
    datos: GastoActualizar,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(solo_admin),
) -> GastoRespuesta:
    gasto = await sesion.get(Gasto, gasto_id)
    if not gasto or gasto.periodo_id != periodo_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")

    periodo = await sesion.get(Periodo, periodo_id)
    if periodo.estado != "abierto":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Solo se pueden editar gastos en periodos abiertos",
        )

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(gasto, campo, valor)

    await sesion.commit()
    await sesion.refresh(gasto)
    return GastoRespuesta.model_validate(gasto)


@router.delete("/{periodo_id}/gastos/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_gasto(
    periodo_id: uuid.UUID,
    gasto_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(solo_admin),
) -> None:
    gasto = await sesion.get(Gasto, gasto_id)
    if not gasto or gasto.periodo_id != periodo_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")

    periodo = await sesion.get(Periodo, periodo_id)
    if periodo.estado != "abierto":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Solo se pueden eliminar gastos en periodos abiertos",
        )

    await sesion.delete(gasto)
    await sesion.commit()


@router.post("/{periodo_id}/liquidar", response_model=LiquidacionRespuesta)
async def liquidar_periodo(
    periodo_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(solo_admin),
) -> LiquidacionRespuesta:
    periodo = await sesion.get(Periodo, periodo_id)
    if not periodo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Periodo no encontrado")
    if periodo.estado != "abierto":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Solo se puede liquidar un periodo abierto",
        )

    # Validar que haya gastos
    resultado_gastos = await sesion.execute(
        select(Gasto).where(Gasto.periodo_id == periodo_id)
    )
    gastos = resultado_gastos.scalars().all()
    if not gastos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No hay gastos registrados en este periodo (AC-9)",
        )

    # Obtener unidades activas con sus propietarios
    resultado_unidades = await sesion.execute(
        select(UnidadFuncional)
        .options(
            selectinload(UnidadFuncional.personas).selectinload(UnidadPersona.persona)
        )
        .where(UnidadFuncional.activa == True)
    )
    unidades = resultado_unidades.scalars().all()

    # Validar que cada unidad tiene propietario vigente (EC-2)
    sin_propietario = [
        u.codigo for u in unidades
        if not any(up.rol == "propietario" and up.vigente for up in u.personas)
    ]
    if sin_propietario:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unidades sin propietario vigente: {', '.join(sin_propietario)}",
        )

    # Calcular totales de gastos
    total_ord = sum(g.monto for g in gastos if g.tipo == "ordinario")
    total_ext = sum(g.monto for g in gastos if g.tipo == "extraordinario")

    # Obtener deudas del periodo anterior cerrado
    deudas = await _obtener_deudas_anteriores(sesion, periodo)

    # Construir datos de calculo
    datos_unidades = [
        DatosUnidad(
            unidad_id=str(u.id),
            indice=u.indice_prorrateo,
            deuda_ordinaria=deudas.get(str(u.id), {}).get("ordinaria", Decimal("0")),
            deuda_extraordinaria=deudas.get(str(u.id), {}).get("extraordinaria", Decimal("0")),
        )
        for u in unidades
    ]

    resultados = calcular_expensas(total_ord, total_ext, datos_unidades)

    # Eliminar liquidacion existente si hay (re-liquidacion)
    # Se usa DELETE directo para evitar problemas de ORM cascade con detalles huerfanos
    liq_existente = await sesion.execute(
        select(Liquidacion).where(Liquidacion.periodo_id == periodo_id)
    )
    liq_anterior = liq_existente.scalar_one_or_none()
    if liq_anterior:
        from sqlalchemy import delete as sql_delete
        await sesion.execute(
            sql_delete(DetalleExpensa).where(DetalleExpensa.liquidacion_id == liq_anterior.id)
        )
        await sesion.execute(
            sql_delete(Liquidacion).where(Liquidacion.id == liq_anterior.id)
        )
        await sesion.flush()

    # Crear nueva liquidacion
    liquidacion = Liquidacion(
        periodo_id=periodo_id,
        gasto_total_ordinario=total_ord,
        gasto_total_extraordinario=total_ext,
    )
    sesion.add(liquidacion)
    await sesion.flush()

    # Crear detalles por unidad
    mapa_unidades = {str(u.id): u for u in unidades}
    detalles = []
    for resultado in resultados:
        unidad = mapa_unidades[resultado.unidad_id]
        detalle = DetalleExpensa(
            liquidacion_id=liquidacion.id,
            unidad_id=unidad.id,
            indice=resultado.indice,
            monto_ordinario=resultado.monto_ordinario,
            monto_extraordinario=resultado.monto_extraordinario,
            deuda_ordinaria=resultado.deuda_ordinaria,
            deuda_extraordinaria=resultado.deuda_extraordinaria,
            total=resultado.total,
        )
        sesion.add(detalle)
        detalles.append(detalle)

    periodo.estado = "liquidado"
    await sesion.commit()
    await sesion.refresh(liquidacion)

    return _construir_respuesta_liquidacion(liquidacion, detalles, mapa_unidades)


async def _obtener_deudas_anteriores(
    sesion: AsyncSession, periodo: Periodo
) -> dict[str, dict[str, Decimal]]:
    """
    Busca el periodo anterior cerrado y devuelve las deudas residuales.
    Por ahora la deuda es el total pendiente (sin modulo de pagos aun).
    En Fase 2 se calculara: total - suma_pagos.
    """
    mes_ant = periodo.mes - 1 if periodo.mes > 1 else 12
    anio_ant = periodo.anio if periodo.mes > 1 else periodo.anio - 1

    resultado = await sesion.execute(
        select(Periodo).where(
            Periodo.consorcio_id == periodo.consorcio_id,
            Periodo.mes == mes_ant,
            Periodo.anio == anio_ant,
            Periodo.estado == "cerrado",
        )
    )
    periodo_ant = resultado.scalar_one_or_none()
    if not periodo_ant or not periodo_ant.liquidacion:
        return {}

    deudas: dict[str, dict[str, Decimal]] = {}
    liq_ant = periodo_ant.liquidacion
    for detalle in liq_ant.detalles:
        # En Fase 1: si no hay pagos, la deuda es el total de la expensa anterior
        # En Fase 2: sera total - pagos recibidos
        deudas[str(detalle.unidad_id)] = {
            "ordinaria": detalle.monto_ordinario + detalle.deuda_ordinaria,
            "extraordinaria": detalle.monto_extraordinario + detalle.deuda_extraordinaria,
        }
    return deudas


def _construir_respuesta_liquidacion(
    liquidacion: Liquidacion,
    detalles: list[DetalleExpensa],
    mapa_unidades: dict[str, UnidadFuncional],
) -> LiquidacionRespuesta:
    detalles_respuesta = []
    for d in detalles:
        unidad = mapa_unidades[str(d.unidad_id)]
        propietario = next(
            (up.persona for up in unidad.personas if up.rol == "propietario" and up.vigente),
            None,
        )
        detalles_respuesta.append(
            DetalleExpensaRespuesta(
                id=d.id,
                unidad_id=d.unidad_id,
                unidad_codigo=unidad.codigo,
                unidad_tipo=unidad.tipo,
                indice=d.indice,
                monto_ordinario=d.monto_ordinario,
                monto_extraordinario=d.monto_extraordinario,
                deuda_ordinaria=d.deuda_ordinaria,
                deuda_extraordinaria=d.deuda_extraordinaria,
                total=d.total,
                propietario_nombre=propietario.nombre_completo if propietario else None,
            )
        )
    return LiquidacionRespuesta(
        id=liquidacion.id,
        periodo_id=liquidacion.periodo_id,
        fecha_generacion=liquidacion.fecha_generacion,
        gasto_total_ordinario=liquidacion.gasto_total_ordinario,
        gasto_total_extraordinario=liquidacion.gasto_total_extraordinario,
        detalles=detalles_respuesta,
    )


@router.get("/{periodo_id}/liquidacion", response_model=LiquidacionRespuesta)
async def obtener_liquidacion(
    periodo_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> LiquidacionRespuesta:
    resultado = await sesion.execute(
        select(Liquidacion)
        .options(
            selectinload(Liquidacion.detalles).selectinload(DetalleExpensa.unidad)
            .selectinload(UnidadFuncional.personas).selectinload(UnidadPersona.persona)
        )
        .where(Liquidacion.periodo_id == periodo_id)
    )
    liquidacion = resultado.scalar_one_or_none()
    if not liquidacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe liquidacion para este periodo",
        )

    mapa_unidades = {str(d.unidad_id): d.unidad for d in liquidacion.detalles}
    return _construir_respuesta_liquidacion(liquidacion, liquidacion.detalles, mapa_unidades)


@router.get("/{periodo_id}/liquidacion/pdf")
async def descargar_pdf_liquidacion(
    periodo_id: uuid.UUID,
    sesion: AsyncSession = Depends(obtener_sesion),
    _: UsuarioActual = Depends(obtener_usuario_actual),
) -> Response:
    resultado = await sesion.execute(
        select(Liquidacion)
        .options(
            selectinload(Liquidacion.detalles).selectinload(DetalleExpensa.unidad)
            .selectinload(UnidadFuncional.personas).selectinload(UnidadPersona.persona),
            selectinload(Liquidacion.periodo),
        )
        .where(Liquidacion.periodo_id == periodo_id)
    )
    liquidacion = resultado.scalar_one_or_none()
    if not liquidacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe liquidacion para este periodo",
        )

    resultado_consorcio = await sesion.execute(
        select(Liquidacion.periodo_id)
    )
    from app.models.consorcio import Consorcio
    resultado_c = await sesion.execute(select(Consorcio).limit(1))
    consorcio = resultado_c.scalar_one_or_none()

    resultado_gastos = await sesion.execute(
        select(Gasto).where(Gasto.periodo_id == periodo_id).order_by(Gasto.fecha)
    )
    gastos = resultado_gastos.scalars().all()

    periodo = liquidacion.periodo
    detalles = sorted(liquidacion.detalles, key=lambda d: d.unidad.tipo + d.unidad.numero)

    detalles_ctx = []
    for d in detalles:
        unidad = d.unidad
        propietario = next(
            (up.persona for up in unidad.personas if up.rol == "propietario" and up.vigente),
            None,
        )
        detalles_ctx.append({
            "unidad_codigo": unidad.codigo,
            "propietario_nombre": propietario.nombre_completo if propietario else None,
            "indice": d.indice,
            "monto_ordinario": d.monto_ordinario,
            "monto_extraordinario": d.monto_extraordinario,
            "deuda_ordinaria": d.deuda_ordinaria,
            "deuda_extraordinaria": d.deuda_extraordinaria,
            "total": d.total,
        })

    hay_deuda_extraordinaria = any(
        float(d["deuda_extraordinaria"]) > 0 for d in detalles_ctx
    )

    from datetime import datetime as dt
    contexto = {
        "consorcio_nombre": consorcio.nombre if consorcio else "Consorcio",
        "consorcio_direccion": consorcio.direccion if consorcio else "",
        "periodo": periodo.etiqueta,
        "fecha_generacion": dt.now().strftime("%d/%m/%Y %H:%M"),
        "gastos": [
            {
                "descripcion": g.descripcion,
                "categoria": g.categoria,
                "tipo": g.tipo,
                "monto": g.monto,
            }
            for g in gastos
        ],
        "gasto_total_ordinario": liquidacion.gasto_total_ordinario,
        "gasto_total_extraordinario": liquidacion.gasto_total_extraordinario,
        "detalles": detalles_ctx,
        "hay_deuda_extraordinaria": hay_deuda_extraordinaria,
        "total_deuda_ordinaria": sum(float(d["deuda_ordinaria"]) for d in detalles_ctx),
        "total_deuda_extraordinaria": sum(float(d["deuda_extraordinaria"]) for d in detalles_ctx),
        "gran_total": sum(float(d["total"]) for d in detalles_ctx),
    }

    pdf_bytes = generar_pdf_liquidacion(contexto)
    nombre_archivo = f"liquidacion-{periodo.anio}-{periodo.mes:02d}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'},
    )
