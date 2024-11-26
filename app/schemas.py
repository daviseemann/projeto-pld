from pydantic import BaseModel
from datetime import datetime


class PLDDataSchema(BaseModel):
    id: str
    submarket: str
    price: float
    timestamp: datetime

    class Config:
        orm_mode = True
