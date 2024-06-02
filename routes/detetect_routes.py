from fastapi import APIRouter
from models.detection import Detection
from config.db import client, collection
from schemas.schema_detection import serializeDict, serializeList
from bson import ObjectId

detection = APIRouter()


@detection.get('/')
async def find_all_detections():
    return serializeList(collection.find())


# @detection.get('/{id}')
# async def find_one_user(id):
#     return serializeDict(conn.local.detection.find_one({"_id":ObjectId(id)}))

@detection.post('/')
def create_detection(detect: Detection):
    collection.insert_one(dict(detect))
    return serializeList(collection.find())


@detection.put('/{id}')
async def update_detection(id, detect: Detection):
    collection.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(detect)
    })
    return serializeDict(collection.find_one({"_id": ObjectId(id)}))


@detection.delete('/{id}')
async def delete_detection(id, detect: Detection):
    return serializeDict(collection.find_one_and_delete({"_id": ObjectId(id)}))
