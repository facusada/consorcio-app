import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class PeriodoCrear(BaseModel):
    mes: int = Field(ge=1, le=12)
    anio: int = Field(ge=2020)


class PeriodoRespuesta(BaseModel):
    id: uuid.UUID
    mes: int
    anio: int
    estado: str
    etiqueta: str
    fecha_cierre: date | None

    model_config = {"from_attributes": True}


class CambioEstado(BaseModel):
    estado: str

    @model_validator(mode="after")
    def validar_estado(self) -> "CambioEstado":
        estados_validos = {"abierto", "liquidado", "cerrado"}
        if self.estado not in estados_validos:
            raise ValueError(f"Estado invalido. Opciones: {estados_validos}")
        return self
