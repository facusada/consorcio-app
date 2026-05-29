import uuid
from decimal import Decimal

from pydantic import BaseModel


class UnidadRespuesta(BaseModel):
    id: uuid.UUID
    tipo: str
    numero: str
    piso: str | None
    indice_prorrateo: Decimal
    activa: bool
    codigo: str

    model_config = {"from_attributes": True}


class UnidadDetalle(UnidadRespuesta):
    propietario_nombre: str | None = None
