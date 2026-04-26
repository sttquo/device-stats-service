from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime


from app.services.analytics import build_device_analytics
from app.schemas.analytics import DeviceAnalyticsResponse
from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementCreate, MeasurementResponse
from app.db.session import SessionLocal
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceResponse

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceResponse)
def create_device(payload: DeviceCreate):
    db: Session = SessionLocal()

    existing_device = db.scalar(
        select(Device).where(Device.external_id == payload.external_id)
    )

    if existing_device:
        db.close()
        raise HTTPException(status_code=400, detail="Device already exists")

    device = Device(external_id=payload.external_id, user_id=payload.user_id)

    db.add(device)
    db.commit()
    db.refresh(device)
    db.close()

    return device


@router.get("/", response_model=list[DeviceResponse])
def get_devices():
    db: Session = SessionLocal()

    devices = db.scalars(select(Device).order_by(Device.id)).all()

    db.close()
    return devices


@router.post("/{external_id}/measurements", response_model=MeasurementResponse)
def create_measurement(external_id: str, payload: MeasurementCreate):
    db: Session = SessionLocal()

    device = db.scalar(select(Device).where(Device.external_id == external_id))
    if not device:
        db.close()
        raise HTTPException(status_code=404, detail="Device not found")

    measurement = Measurement(
        device_id=device.id, x=payload.x, y=payload.y, z=payload.z
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    db.close()

    return measurement


@router.get("/{external_id}/analytics", response_model=DeviceAnalyticsResponse)
def get_device_analytics(
    external_id: str,
    start_at: datetime | None = None,
    end_at: datetime | None = None,
):

    db: Session = SessionLocal()
    device = db.scalar(select(Device).where(Device.external_id == external_id))
    if not device:
        db.close()
        raise HTTPException(status_code=404, detail="Device not found")

    query = select(Measurement).where(Measurement.device_id == device.id)

    if start_at:
        query = query.where(Measurement.created_at >= start_at)
    if end_at:
        query = query.where(Measurement.created_at <= end_at)

    measurements = db.scalars(query).all()

    analytics = build_device_analytics(measurements)
    db.close()
    return analytics
