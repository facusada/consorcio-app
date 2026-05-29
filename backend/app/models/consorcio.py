import uuid
from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Consorcio(Base):
    __tablename__ = "consorcios"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    direccion: Mapped[str] = mapped_column(String(300), nullable=False)
    localidad: Mapped[str] = mapped_column(String(100), nullable=False)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, default="Buenos Aires")
    cuit: Mapped[str | None] = mapped_column(String(13), unique=True, nullable=True)
    reglamento_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    unidades: Mapped[list["UnidadFuncional"]] = relationship(back_populates="consorcio")
    periodos: Mapped[list["Periodo"]] = relationship(back_populates="consorcio")
