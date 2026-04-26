from pydantic import BaseModel


class DeviceCreate(BaseModel):
    external_id: str
    user_id: int | None = None


class DeviceResponse(BaseModel):
    id: int
    external_id: str
    user_id: int | None = None

    model_config = {"from_attributes": True}
