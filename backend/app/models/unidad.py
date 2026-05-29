import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Decimal as SADecimal, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UnidadFuncional(Base):
    __tablename__ = "unidades_funcionales"
    __table_args__ = (
        UniqueConstraint("consorcio_id", "tipo", "numero", name="uq_unidad_consorcio_tipo_numero"),
        CheckConstraint("tipo IN ('departamento', 'cochera')", name="ck_unidad_tipo"),
        CheckConstraint(
            "indice_prorrateo > 0 AND indice_prorrateo <= 100",
            name="ck_unidad_indice",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    consorcio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("consorcios.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    numero: Mapped[str] = mapped_column(String(10), nullable=False)
    piso: Mapped[str | None] = mapped_column(String(10), nullable=True)
    indice_prorrateo: Mapped[Decimal] = mapped_column(SADecimal(5, 2), nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    consorcio: Mapped["Consorcio"] = relationship(back_populates="unidades")
    personas: Mapped[list["UnidadPersona"]] = relationship(back_populates="unidad")
    detalles_expensa: Mapped[list["DetalleExpensa"]] = relationship(back_populates="unidad")

    @property
    def codigo(self) -> str:
        if self.tipo == "departamento":
            return f"DEPTO-{self.numero}"
        return f"COCH-{self.numero}"
