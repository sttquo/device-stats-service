from datetime import datetime
from pydantic import BaseModel


class MeasurementCreate(BaseModel):
    x: float
    y: float
    z: float


class MeasurementResponse(BaseModel):
    id: int
    device_id: int
    x: float
    y: float
    z: float
    created_at: datetime

    model_config = {"from_attributes": True}
