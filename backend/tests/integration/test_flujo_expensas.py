"""
Tests de integracion del flujo completo de expensas.
Validan los criterios de aceptacion AC-1 a AC-10 de la spec SDD.
Requieren PostgreSQL en DATABASE_URL (o DATABASE_URL_TEST).
"""
import pytest


pytestmark = pytest.mark.asyncio


class TestAutenticacion:
    async def test_login_exitoso(self, cliente, datos_base):
        resp = await cliente.post(
            "/api/v1/auth/login",
            json={"email": datos_base["admin_email"], "contrasena": "Admin1234!"},
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_login_credenciales_incorrectas(self, cliente, datos_base):
        resp = await cliente.post(
            "/api/v1/auth/login",
            json={"email": datos_base["admin_email"], "contrasena": "mal"},
        )
        assert resp.status_code == 401

    async def test_ruta_protegida_sin_token(self, cliente):
        resp = await cliente.get("/api/v1/periodos")
        assert resp.status_code == 403

    async def test_me_retorna_usuario(self, cliente, token_admin):
        resp = await cliente.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 200
        assert resp.json()["rol"] == "admin"


class TestPeriodos:
    async def test_crear_periodo(self, cliente, token_admin):
        resp = await cliente.post(
            "/api/v1/periodos",
            json={"mes": 4, "anio": 2026},
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["mes"] == 4
        assert data["anio"] == 2026
        assert data["estado"] == "abierto"
        assert data["etiqueta"] == "Abril 2026"

    async def test_periodo_duplicado_falla(self, cliente, token_admin):
        await cliente.post(
            "/api/v1/periodos",
            json={"mes": 5, "anio": 2026},
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        resp = await cliente.post(
            "/api/v1/periodos",
            json={"mes": 5, "anio": 2026},
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 409

    async def test_listar_periodos(self, cliente, token_admin):
        resp = await cliente.get(
            "/api/v1/periodos",
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestGastos:
    @pytest.fixture(autouse=True)
    async def periodo_abierto(self, cliente, token_admin):
        resp = await cliente.post(
            "/api/v1/periodos",
            json={"mes": 6, "anio": 2026},
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        self.periodo_id = resp.json()["id"]
        self.headers = {"Authorization": f"Bearer {token_admin}"}

    async def test_agregar_gasto(self, cliente):
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/gastos",
            json={
                "descripcion": "Servicio de limpieza",
                "monto": 50000,
                "tipo": "ordinario",
                "categoria": "limpieza",
                "fecha": "2026-06-01",
            },
            headers=self.headers,
        )
        assert resp.status_code == 201
        assert resp.json()["monto"] == "50000.00"

    async def test_gasto_monto_cero_falla(self, cliente):
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/gastos",
            json={
                "descripcion": "Gasto invalido",
                "monto": 0,
                "tipo": "ordinario",
                "categoria": "otros",
                "fecha": "2026-06-01",
            },
            headers=self.headers,
        )
        assert resp.status_code == 422

    async def test_eliminar_gasto(self, cliente):
        resp_crear = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/gastos",
            json={
                "descripcion": "Gasto a eliminar",
                "monto": 1000,
                "tipo": "ordinario",
                "categoria": "otros",
                "fecha": "2026-06-01",
            },
            headers=self.headers,
        )
        gasto_id = resp_crear.json()["id"]
        resp_del = await cliente.delete(
            f"/api/v1/periodos/{self.periodo_id}/gastos/{gasto_id}",
            headers=self.headers,
        )
        assert resp_del.status_code == 204


class TestLiquidacion:
    """AC-1 a AC-9: validacion del calculo completo con datos reales."""

    @pytest.fixture(autouse=True)
    async def preparar_periodo(self, cliente, token_admin):
        resp = await cliente.post(
            "/api/v1/periodos",
            json={"mes": 7, "anio": 2026},
            headers={"Authorization": f"Bearer {token_admin}"},
        )
        self.periodo_id = resp.json()["id"]
        self.headers = {"Authorization": f"Bearer {token_admin}"}

        await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/gastos",
            json={
                "descripcion": "Gastos ordinarios totales",
                "monto": 345000,
                "tipo": "ordinario",
                "categoria": "servicios",
                "fecha": "2026-07-01",
            },
            headers=self.headers,
        )

    async def test_liquidar_periodo(self, cliente):
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["gasto_total_ordinario"] == "345000.00"
        assert len(data["detalles"]) == 13

    async def test_ac1_montos_correctos_abril_2026(self, cliente):
        """AC-1: los montos calculados deben coincidir con el Excel de abril 2026."""
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        detalles = resp.json()["detalles"]
        montos = {d["unidad_codigo"]: float(d["monto_ordinario"]) for d in detalles}

        assert montos["DEPTO-1"] == pytest.approx(57546.00)
        assert montos["DEPTO-2"] == pytest.approx(45298.50)
        assert montos["COCH-A"] == pytest.approx(2932.50)
        assert montos["COCH-F"] == pytest.approx(3277.50)

    async def test_ac5_suma_igual_al_total(self, cliente):
        """AC-5: la suma de las expensas ordinarias debe igualar el gasto total."""
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        detalles = resp.json()["detalles"]
        suma = sum(float(d["monto_ordinario"]) for d in detalles)
        assert suma == pytest.approx(345000.00)

    async def test_ac9_sin_gastos_no_se_puede_liquidar(self, cliente, token_admin):
        """AC-9: liquidar sin gastos debe retornar error."""
        resp_periodo = await cliente.post(
            "/api/v1/periodos",
            json={"mes": 8, "anio": 2026},
            headers=self.headers,
        )
        periodo_vacio_id = resp_periodo.json()["id"]
        resp = await cliente.post(
            f"/api/v1/periodos/{periodo_vacio_id}/liquidar",
            headers=self.headers,
        )
        assert resp.status_code == 422

    async def test_ac6_periodo_cerrado_no_acepta_gastos(self, cliente):
        """AC-6: un periodo cerrado no puede recibir nuevos gastos."""
        await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        await cliente.patch(
            f"/api/v1/periodos/{self.periodo_id}/estado",
            json={"estado": "cerrado"},
            headers=self.headers,
        )
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/gastos",
            json={
                "descripcion": "Gasto prohibido",
                "monto": 1000,
                "tipo": "ordinario",
                "categoria": "otros",
                "fecha": "2026-07-15",
            },
            headers=self.headers,
        )
        assert resp.status_code == 422

    async def test_ac8_reliquidacion_reemplaza_anterior(self, cliente):
        """AC-8: se puede reabrir un periodo liquidado y re-liquidar."""
        await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        await cliente.patch(
            f"/api/v1/periodos/{self.periodo_id}/estado",
            json={"estado": "abierto"},
            headers=self.headers,
        )
        resp = await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        assert resp.status_code == 200
        detalles = resp.json()["detalles"]
        assert len(detalles) == 13

    async def test_transicion_estado_invalida(self, cliente):
        """Un periodo cerrado no puede volver a abierto."""
        await cliente.post(
            f"/api/v1/periodos/{self.periodo_id}/liquidar",
            headers=self.headers,
        )
        await cliente.patch(
            f"/api/v1/periodos/{self.periodo_id}/estado",
            json={"estado": "cerrado"},
            headers=self.headers,
        )
        resp = await cliente.patch(
            f"/api/v1/periodos/{self.periodo_id}/estado",
            json={"estado": "abierto"},
            headers=self.headers,
        )
        assert resp.status_code == 422
