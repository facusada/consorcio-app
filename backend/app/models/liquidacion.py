import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Liquidacion(Base):
    __tablename__ = "liquidaciones"
    __table_args__ = (
        CheckConstraint("gasto_total_ordinario >= 0", name="ck_liquidacion_ordinario"),
        CheckConstraint("gasto_total_extraordinario >= 0", name="ck_liquidacion_extraordinario"),
        Index("ix_liquidacion_periodo_id", "periodo_id", unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    periodo_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("periodos.id"), unique=True, nullable=False
    )
    fecha_generacion: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    gasto_total_ordinario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    gasto_total_extraordinario: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    periodo: Mapped["Periodo"] = relationship(back_populates="liquidacion")
    detalles: Mapped[list["DetalleExpensa"]] = relationship(back_populates="liquidacion")
