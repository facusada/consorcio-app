from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import configuracion

motor = create_async_engine(configuracion.database_url, echo=False)

SessionLocal = async_sessionmaker(
    bind=motor,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def obtener_sesion() -> AsyncSession:
    async with SessionLocal() as sesion:
        yield sesion
