import uuid
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Persona(Base):
    __tablename__ = "personas"
    __table_args__ = (
        CheckConstraint("tipo IN ('propietario', 'inquilino')", name="ck_persona_tipo"),
        Index("ix_persona_email", "email", unique=True, postgresql_where="email IS NOT NULL"),
        Index("ix_persona_apellido", "apellido"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    unidades: Mapped[list["UnidadPersona"]] = relationship(back_populates="persona")
    usuario: Mapped["Usuario | None"] = relationship(back_populates="persona", uselist=False)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"
