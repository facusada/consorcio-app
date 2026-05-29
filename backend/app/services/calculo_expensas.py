"""
Logica de calculo de expensas.

Implementa las reglas de negocio definidas en docs/sdd/wip/expensas/spec.md:
- RN-1: distribucion por indice de prorrateo
- RN-4: calculo del total por unidad
- RN-9: redondeo con ajuste en la unidad de mayor indice
"""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass
class DatosUnidad:
    unidad_id: str
    indice: Decimal
    deuda_ordinaria: Decimal = Decimal("0")
    deuda_extraordinaria: Decimal = Decimal("0")


@dataclass
class ResultadoUnidad:
    unidad_id: str
    indice: Decimal
    monto_ordinario: Decimal
    monto_extraordinario: Decimal
    deuda_ordinaria: Decimal
    deuda_extraordinaria: Decimal
    total: Decimal


def calcular_expensas(
    gasto_total_ordinario: Decimal,
    gasto_total_extraordinario: Decimal,
    unidades: list[DatosUnidad],
) -> list[ResultadoUnidad]:
    """
    Calcula la expensa de cada unidad aplicando el indice de prorrateo.
    Aplica RN-9: si la suma de montos redondeados no coincide con el total,
    la diferencia se ajusta en la unidad de mayor indice.
    """
    if not unidades:
        return []

    centavos = Decimal("0.01")
    resultados = []

    for unidad in unidades:
        monto_ord = (gasto_total_ordinario * unidad.indice / Decimal("100")).quantize(
            centavos, rounding=ROUND_HALF_UP
        )
        monto_ext = (gasto_total_extraordinario * unidad.indice / Decimal("100")).quantize(
            centavos, rounding=ROUND_HALF_UP
        )
        resultados.append(
            ResultadoUnidad(
                unidad_id=unidad.unidad_id,
                indice=unidad.indice,
                monto_ordinario=monto_ord,
                monto_extraordinario=monto_ext,
                deuda_ordinaria=unidad.deuda_ordinaria,
                deuda_extraordinaria=unidad.deuda_extraordinaria,
                total=monto_ord + monto_ext + unidad.deuda_ordinaria + unidad.deuda_extraordinaria,
            )
        )

    _ajustar_redondeo(resultados, gasto_total_ordinario, gasto_total_extraordinario)

    return resultados


def _ajustar_redondeo(
    resultados: list[ResultadoUnidad],
    total_ordinario: Decimal,
    total_extraordinario: Decimal,
) -> None:
    """
    Si la suma de las partes no coincide con el total (diferencia de centavos),
    ajusta en la unidad de mayor indice (RN-9).
    """
    if not resultados:
        return

    suma_ord = sum(r.monto_ordinario for r in resultados)
    suma_ext = sum(r.monto_extraordinario for r in resultados)

    diff_ord = total_ordinario - suma_ord
    diff_ext = total_extraordinario - suma_ext

    if diff_ord == 0 and diff_ext == 0:
        return

    unidad_mayor_indice = max(resultados, key=lambda r: r.indice)

    if diff_ord != 0:
        unidad_mayor_indice.monto_ordinario += diff_ord

    if diff_ext != 0:
        unidad_mayor_indice.monto_extraordinario += diff_ext

    unidad_mayor_indice.total = (
        unidad_mayor_indice.monto_ordinario
        + unidad_mayor_indice.monto_extraordinario
        + unidad_mayor_indice.deuda_ordinaria
        + unidad_mayor_indice.deuda_extraordinaria
    )
