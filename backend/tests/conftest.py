"""
Fixtures compartidas para tests de integracion.
Requiere PostgreSQL en DATABASE_URL (por defecto consorcio_test).

NullPool es obligatorio con pytest-asyncio: cada test crea su propio event loop
y el pool por defecto de asyncpg se ata al loop que lo creo.
"""
import asyncio
import os
from datetime import date
from decimal import Decimal

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

DATABASE_URL_TEST = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://consorcio:consorcio@localhost:5432/consorcio_test",
)


def _setup_tablas() -> None:
    import app.models  # noqa: F401

    from app.core.database import Base

    async def _crear():
        engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    asyncio.run(_crear())


_setup_tablas()

TABLAS_A_LIMPIAR = [
    "detalles_expensa", "liquidaciones", "gastos", "periodos",
    "unidades_personas", "usuarios", "personas", "unidades_funcionales", "consorcios",
]


def _motor():
    return create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)


@pytest_asyncio.fixture(autouse=True)
async def limpiar_db():
    """Trunca todas las tablas antes de cada test para aislar el estado."""
    engine = _motor()
    async with engine.begin() as conn:
        for tabla in TABLAS_A_LIMPIAR:
            await conn.execute(
                __import__("sqlalchemy").text(f'TRUNCATE TABLE "{tabla}" CASCADE')
            )
    await engine.dispose()
    yield


@pytest_asyncio.fixture
async def sesion() -> AsyncSession:
    engine = _motor()
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as s:
        yield s
        await s.rollback()
    await engine.dispose()


@pytest_asyncio.fixture
async def cliente(sesion: AsyncSession):
    from app.core.database import obtener_sesion
    from app.main import app

    async def _override():
        yield sesion

    app.dependency_overrides[obtener_sesion] = _override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def datos_base(sesion: AsyncSession):
    from app.core.seguridad import hashear_contrasena
    from app.models.consorcio import Consorcio
    from app.models.persona import Persona
    from app.models.unidad import UnidadFuncional
    from app.models.unidad_persona import UnidadPersona
    from app.models.usuario import Usuario

    consorcio = Consorcio(
        nombre="Consorcio Test",
        direccion="Calle Test 123",
        localidad="Buenos Aires",
        provincia="Buenos Aires",
    )
    sesion.add(consorcio)
    await sesion.flush()

    specs_unidades = [
        ("departamento", "1", None, "16.68"),
        ("departamento", "2", None, "13.13"),
        ("departamento", "3", None, "12.91"),
        ("departamento", "4", None, "13.13"),
        ("departamento", "5", None, "12.91"),
        ("departamento", "6", None, "13.13"),
        ("departamento", "7", None, "12.91"),
        ("cochera", "A", None, "0.85"),
        ("cochera", "B", None, "0.85"),
        ("cochera", "C", None, "0.85"),
        ("cochera", "D", None, "0.85"),
        ("cochera", "E", None, "0.85"),
        ("cochera", "F", None, "0.95"),
    ]
    unidades = []
    for tipo, numero, piso, indice in specs_unidades:
        u = UnidadFuncional(
            consorcio_id=consorcio.id,
            tipo=tipo,
            numero=numero,
            piso=piso,
            indice_prorrateo=Decimal(indice),
        )
        sesion.add(u)
        unidades.append(u)

    await sesion.flush()

    propietarios_seed = [
        ("Pamela", "Pitscheider", 0),
        ("Elena", "Michailenko", 1),
        ("Elena", "Michailenko", 2),
        ("Elena", "Michailenko", 3),
        ("Eliana", "Iafolla", 4),
        ("Eliana", "Iafolla", 5),
        ("Claudio", "Ghida", 6),
        ("Maria", "Duarte", 7),
        ("Maria", "Duarte", 8),
        ("Graciela", "Farina", 9),
        ("Graciela", "Farina", 10),
        ("Lautaro", "Villordo", 11),
        ("Lautaro", "Villordo", 12),
    ]

    personas_cache: dict[str, Persona] = {}
    for nombre, apellido, idx in propietarios_seed:
        clave = f"{nombre} {apellido}"
        if clave not in personas_cache:
            p = Persona(nombre=nombre, apellido=apellido, tipo="propietario")
            sesion.add(p)
            await sesion.flush()
            personas_cache[clave] = p
        up = UnidadPersona(
            unidad_id=unidades[idx].id,
            persona_id=personas_cache[clave].id,
            rol="propietario",
            fecha_desde=date(2024, 1, 1),
        )
        sesion.add(up)

    persona_admin = Persona(nombre="Admin", apellido="Sistema", tipo="propietario")
    sesion.add(persona_admin)
    await sesion.flush()

    admin = Usuario(
        persona_id=persona_admin.id,
        email="admin@test.local",
        password_hash=hashear_contrasena("Admin1234!"),
        rol="admin",
    )
    sesion.add(admin)
    await sesion.commit()

    return {
        "consorcio": consorcio,
        "unidades": unidades,
        "admin_email": "admin@test.local",
        "admin_password": "Admin1234!",
    }


@pytest_asyncio.fixture
async def token_admin(cliente, datos_base):
    resp = await cliente.post(
        "/api/v1/auth/login",
        json={
            "email": datos_base["admin_email"],
            "contrasena": datos_base["admin_password"],
        },
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]
