from pydantic import BaseModel
from datetime import datetime


class Detection(BaseModel):
    name: str
    date: datetime
    image: str
    description: str
    detections: list
