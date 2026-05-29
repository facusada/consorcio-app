import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DetalleExpensa(Base):
    __tablename__ = "detalles_expensa"
    __table_args__ = (
        UniqueConstraint("liquidacion_id", "unidad_id", name="uq_detalle_liquidacion_unidad"),
        CheckConstraint("monto_ordinario >= 0", name="ck_detalle_ordinario"),
        CheckConstraint("monto_extraordinario >= 0", name="ck_detalle_extraordinario"),
        CheckConstraint("deuda_ordinaria >= 0", name="ck_detalle_deuda_ordinaria"),
        CheckConstraint("deuda_extraordinaria >= 0", name="ck_detalle_deuda_extraordinaria"),
        CheckConstraint("total >= 0", name="ck_detalle_total"),
        Index("ix_detalle_liquidacion_id", "liquidacion_id"),
        Index("ix_detalle_unidad_id", "unidad_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    liquidacion_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("liquidaciones.id"), nullable=False
    )
    unidad_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("unidades_funcionales.id"), nullable=False
    )
    indice: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    monto_ordinario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    monto_extraordinario: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    deuda_ordinaria: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    deuda_extraordinaria: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    liquidacion: Mapped["Liquidacion"] = relationship(back_populates="detalles")
    unidad: Mapped["UnidadFuncional"] = relationship(back_populates="detalles_expensa")
