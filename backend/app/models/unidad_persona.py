import uuid
from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UnidadPersona(Base):
    __tablename__ = "unidades_personas"
    __table_args__ = (
        CheckConstraint("rol IN ('propietario', 'inquilino')", name="ck_unidad_persona_rol"),
        CheckConstraint(
            "fecha_hasta IS NULL OR fecha_hasta >= fecha_desde",
            name="ck_unidad_persona_fechas",
        ),
        Index("ix_unidad_persona_unidad_id", "unidad_id"),
        Index("ix_unidad_persona_persona_id", "persona_id"),
        Index(
            "ix_unidad_persona_vigente",
            "unidad_id",
            "rol",
            postgresql_where="fecha_hasta IS NULL",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    unidad_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("unidades_funcionales.id"), nullable=False)
    persona_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("personas.id"), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_desde: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_hasta: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    unidad: Mapped["UnidadFuncional"] = relationship(back_populates="personas")
    persona: Mapped["Persona"] = relationship(back_populates="unidades")

    @property
    def vigente(self) -> bool:
        return self.fecha_hasta is None
