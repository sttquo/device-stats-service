from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.device import Device
from app.models.measurement import Measurement
from app.schemas.device import DeviceResponse
from app.schemas.user import UserCreate, UserResponse
from app.schemas.analytics import UserAnalyticsResponse
from app.services.analytics import build_device_analytics

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate):
    db: Session = SessionLocal()

    user = User(name=payload.name)

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return user


@router.get("/", response_model=list[UserResponse])
def get_users():
    db: Session = SessionLocal()

    users = db.scalars(select(User).order_by(User.id)).all()

    db.close()
    return users


@router.post("/{user_id}/devices/{external_id}", response_model=DeviceResponse)
def attach_device_to_user(user_id: int, external_id: str):
    db: Session = SessionLocal()

    user = db.get(User, user_id)
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    device = db.scalar(select(Device).where(Device.external_id == external_id))
    if not device:
        db.close()
        raise HTTPException(status_code=404, detail="Device not found")
    device.user_id = user_id

    db.commit()
    db.refresh(device)
    db.close()

    return device


@router.get("/{user_id}/analytics", response_model=UserAnalyticsResponse)
def get_user_analytics(user_id: int):
    db: Session = SessionLocal()

    user = db.get(User, user_id)
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    devices = db.scalars(
        select(Device).where(Device.user_id == user_id).order_by(Device.id)
    ).all()

    devices_analytics = {}
    all_measurements = []

    for device in devices:
        measurements = db.scalars(
            select(Measurement).where(Measurement.device_id == device.id)
        ).all()

        devices_analytics[device.external_id] = build_device_analytics(measurements)
        all_measurements.extend(measurements)

    aggregate_analytics = build_device_analytics(all_measurements)
    db.close()

    return UserAnalyticsResponse(
        aggregated=aggregate_analytics,
        devices=devices_analytics,
    )
