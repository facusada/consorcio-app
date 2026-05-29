import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class DetalleExpensaRespuesta(BaseModel):
    id: uuid.UUID
    unidad_id: uuid.UUID
    unidad_codigo: str
    unidad_tipo: str
    indice: Decimal
    monto_ordinario: Decimal
    monto_extraordinario: Decimal
    deuda_ordinaria: Decimal
    deuda_extraordinaria: Decimal
    total: Decimal
    propietario_nombre: str | None = None

    model_config = {"from_attributes": True}


class LiquidacionRespuesta(BaseModel):
    id: uuid.UUID
    periodo_id: uuid.UUID
    fecha_generacion: datetime
    gasto_total_ordinario: Decimal
    gasto_total_extraordinario: Decimal
    detalles: list[DetalleExpensaRespuesta]

    model_config = {"from_attributes": True}
