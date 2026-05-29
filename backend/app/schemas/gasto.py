import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


CATEGORIAS_VALIDAS = {
    "servicios", "limpieza", "mantenimiento", "seguros",
    "impuestos", "honorarios", "extraordinario", "otros",
}

TIPOS_VALIDOS = {"ordinario", "extraordinario"}


class GastoCrear(BaseModel):
    descripcion: str = Field(min_length=3, max_length=300)
    monto: Decimal = Field(gt=0)
    tipo: str
    categoria: str
    fecha: date

    def model_post_init(self, __context) -> None:
        if self.tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo invalido. Opciones: {TIPOS_VALIDOS}")
        if self.categoria not in CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria invalida. Opciones: {CATEGORIAS_VALIDAS}")


class GastoActualizar(BaseModel):
    descripcion: str | None = Field(default=None, min_length=3, max_length=300)
    monto: Decimal | None = Field(default=None, gt=0)
    tipo: str | None = None
    categoria: str | None = None
    fecha: date | None = None


class GastoRespuesta(BaseModel):
    id: uuid.UUID
    descripcion: str
    monto: Decimal
    tipo: str
    categoria: str
    fecha: date

    model_config = {"from_attributes": True}
