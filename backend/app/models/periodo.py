import uuid
from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Periodo(Base):
    __tablename__ = "periodos"
    __table_args__ = (
        UniqueConstraint("consorcio_id", "mes", "anio", name="uq_periodo_consorcio_mes_anio"),
        CheckConstraint("mes BETWEEN 1 AND 12", name="ck_periodo_mes"),
        CheckConstraint("anio >= 2020", name="ck_periodo_anio"),
        CheckConstraint(
            "estado IN ('abierto', 'liquidado', 'cerrado')", name="ck_periodo_estado"
        ),
        Index("ix_periodo_consorcio_id", "consorcio_id"),
        Index("ix_periodo_estado", "estado"),
        Index("ix_periodo_anio_mes", "anio", "mes"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    consorcio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("consorcios.id"), nullable=False)
    mes: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    anio: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="abierto")
    fecha_cierre: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    consorcio: Mapped["Consorcio"] = relationship(back_populates="periodos")
    gastos: Mapped[list["Gasto"]] = relationship(back_populates="periodo")
    liquidacion: Mapped["Liquidacion | None"] = relationship(
        back_populates="periodo", uselist=False
    )

    @property
    def etiqueta(self) -> str:
        meses = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
        ]
        return f"{meses[self.mes]} {self.anio}"
