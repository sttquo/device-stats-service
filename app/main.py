from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.devices import router as devices_router
from app.db.base import Base
from app.db.session import engine
from app.models.device import Device
from app.models.measurement import Measurement
from app.models.user import User

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(users_router)
app.include_router(devices_router)


@app.get("/")
def read_root():
    return {"message": "Service is running"}
