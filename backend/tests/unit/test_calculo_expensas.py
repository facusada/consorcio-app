"""
Tests unitarios del servicio de calculo de expensas.

Validan las reglas de negocio RN-1, RN-4, RN-9 de la spec SDD.
Los valores esperados provienen de los datos reales del consorcio (abril 2026).
"""
from decimal import Decimal

import pytest

from app.services.calculo_expensas import DatosUnidad, calcular_expensas


# Indices reales del consorcio (suman 100.00%)
UNIDADES_CONSORCIO = [
    DatosUnidad("depto-1", Decimal("16.68")),
    DatosUnidad("depto-2", Decimal("13.13")),
    DatosUnidad("depto-3", Decimal("12.91")),
    DatosUnidad("depto-4", Decimal("13.13")),
    DatosUnidad("depto-5", Decimal("12.91")),
    DatosUnidad("depto-6", Decimal("13.13")),
    DatosUnidad("depto-7", Decimal("12.91")),
    DatosUnidad("coch-a", Decimal("0.85")),
    DatosUnidad("coch-b", Decimal("0.85")),
    DatosUnidad("coch-c", Decimal("0.85")),
    DatosUnidad("coch-d", Decimal("0.85")),
    DatosUnidad("coch-e", Decimal("0.85")),
    DatosUnidad("coch-f", Decimal("0.95")),
]


class TestCalculoExpensasAbril2026:
    """AC-1: calculo correcto con datos reales de abril 2026."""

    def test_depto1_expensa_ordinaria(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        depto1 = next(r for r in resultados if r.unidad_id == "depto-1")
        assert depto1.monto_ordinario == Decimal("57546.00")

    def test_depto2_expensa_ordinaria(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        depto2 = next(r for r in resultados if r.unidad_id == "depto-2")
        assert depto2.monto_ordinario == Decimal("45298.50")

    def test_cochera_a_expensa_ordinaria(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        coch_a = next(r for r in resultados if r.unidad_id == "coch-a")
        assert coch_a.monto_ordinario == Decimal("2932.50")

    def test_cochera_f_expensa_ordinaria(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        coch_f = next(r for r in resultados if r.unidad_id == "coch-f")
        assert coch_f.monto_ordinario == Decimal("3277.50")

    def test_suma_montos_igual_gasto_total(self):
        """AC-5: la suma de expensas ordinarias debe ser igual al gasto total."""
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        suma = sum(r.monto_ordinario for r in resultados)
        assert suma == Decimal("345000.00")

    def test_todas_las_unidades_tienen_detalle(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        assert len(resultados) == 13


class TestDeudaAcumulada:
    """AC-2: deuda acumulada se suma correctamente al total."""

    def test_depto6_con_deuda_acumulada(self):
        unidades = list(UNIDADES_CONSORCIO)
        unidades[5] = DatosUnidad(
            "depto-6", Decimal("13.13"), deuda_ordinaria=Decimal("108895.00")
        )
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), unidades)
        depto6 = next(r for r in resultados if r.unidad_id == "depto-6")
        assert depto6.deuda_ordinaria == Decimal("108895.00")
        assert depto6.monto_ordinario == Decimal("45298.50")
        assert depto6.total == Decimal("154193.50")

    def test_sin_deuda_total_igual_a_expensa(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        depto1 = next(r for r in resultados if r.unidad_id == "depto-1")
        assert depto1.total == depto1.monto_ordinario


class TestExpensasExtraordinarias:
    """RN-3: expensas ordinarias y extraordinarias se calculan de forma independiente."""

    def test_gasto_extraordinario_distribuido(self):
        unidades = [
            DatosUnidad("u1", Decimal("50.00")),
            DatosUnidad("u2", Decimal("50.00")),
        ]
        resultados = calcular_expensas(Decimal("100"), Decimal("200"), unidades)
        assert resultados[0].monto_ordinario == Decimal("50.00")
        assert resultados[0].monto_extraordinario == Decimal("100.00")
        assert resultados[0].total == Decimal("150.00")

    def test_sin_extraordinarios_monto_cero(self):
        resultados = calcular_expensas(Decimal("345000"), Decimal("0"), UNIDADES_CONSORCIO)
        for r in resultados:
            assert r.monto_extraordinario == Decimal("0.00")


class TestRedondeo:
    """RN-9: redondeo con ajuste en unidad de mayor indice."""

    def test_suma_siempre_igual_al_total(self):
        """Con cualquier monto, la suma debe ser exacta."""
        unidades = [
            DatosUnidad("u1", Decimal("33.33")),
            DatosUnidad("u2", Decimal("33.33")),
            DatosUnidad("u3", Decimal("33.34")),
        ]
        total = Decimal("1000")
        resultados = calcular_expensas(total, Decimal("0"), unidades)
        suma = sum(r.monto_ordinario for r in resultados)
        assert suma == total

    def test_diferencia_ajusta_en_mayor_indice(self):
        unidades = [
            DatosUnidad("menor", Decimal("33.33")),
            DatosUnidad("mayor", Decimal("66.67")),
        ]
        total = Decimal("1")
        resultados = calcular_expensas(total, Decimal("0"), unidades)
        suma = sum(r.monto_ordinario for r in resultados)
        assert suma == total


class TestCasosEdge:
    """Edge cases de la spec."""

    def test_lista_vacia_retorna_vacia(self):
        resultados = calcular_expensas(Decimal("1000"), Decimal("0"), [])
        assert resultados == []

    def test_una_sola_unidad_recibe_todo(self):
        unidades = [DatosUnidad("u1", Decimal("100.00"))]
        resultados = calcular_expensas(Decimal("1000"), Decimal("0"), unidades)
        assert resultados[0].monto_ordinario == Decimal("1000.00")

    def test_gasto_total_cero_produce_montos_cero(self):
        resultados = calcular_expensas(Decimal("0"), Decimal("0"), UNIDADES_CONSORCIO)
        for r in resultados:
            assert r.monto_ordinario == Decimal("0.00")
            assert r.monto_extraordinario == Decimal("0.00")
