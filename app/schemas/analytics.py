from pydantic import BaseModel


class MetricStats(BaseModel):
    min: float | None
    max: float | None
    count: int
    sum: float
    median: float | None


class DeviceAnalyticsResponse(BaseModel):
    x: MetricStats
    y: MetricStats
    z: MetricStats


class UserAnalyticsResponse(BaseModel):
    aggregated: DeviceAnalyticsResponse
    devices: dict[str, DeviceAnalyticsResponse]
