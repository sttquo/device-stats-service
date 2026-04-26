from statistics import median
from collections.abc import Sequence

from app.models.measurement import Measurement
from app.schemas.analytics import DeviceAnalyticsResponse, MetricStats


def calculate_metric_stats(values: list[float]) -> MetricStats:
    if not values:
        return MetricStats(
            min=None,
            max=None,
            count=0,
            sum=0.0,
            median=None,
        )
    return MetricStats(
        min=min(values),
        max=max(values),
        count=len(values),
        sum=float(sum(values)),
        median=float(median(values)),
    )


def build_device_analytics(
    measurements: Sequence[Measurement],
) -> DeviceAnalyticsResponse:
    x_values = [measurements.x for measurements in measurements]
    y_values = [measurements.y for measurements in measurements]
    z_values = [measurements.z for measurements in measurements]

    return DeviceAnalyticsResponse(
        x=calculate_metric_stats(x_values),
        y=calculate_metric_stats(y_values),
        z=calculate_metric_stats(z_values),
    )
