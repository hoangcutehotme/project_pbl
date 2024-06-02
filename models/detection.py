from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime


class Detection(BaseModel):
    name: str
    date: datetime
    image: str
    description: str
    detections: list

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data
