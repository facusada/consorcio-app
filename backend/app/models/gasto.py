import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Decimal as SADecimal, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Gasto(Base):
    __tablename__ = "gastos"
    __table_args__ = (
        CheckConstraint("tipo IN ('ordinario', 'extraordinario')", name="ck_gasto_tipo"),
        CheckConstraint("monto > 0", name="ck_gasto_monto_positivo"),
        Index("ix_gasto_periodo_id", "periodo_id"),
        Index("ix_gasto_tipo", "tipo"),
        Index("ix_gasto_categoria", "categoria"),
        Index("ix_gasto_fecha", "fecha"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    periodo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("periodos.id"), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(300), nullable=False)
    monto: Mapped[Decimal] = mapped_column(SADecimal(12, 2), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    comprobante_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    periodo: Mapped["Periodo"] = relationship(back_populates="gastos")
