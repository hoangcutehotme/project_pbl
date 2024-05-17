# Normal way

def detectionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "date": item["date"],
        "image": item['image'],
        "description": item["description"],
        "detections": item["detection"]
    }


def detectionsEntity(entity) -> list:
    return [detectionEntity(item) for item in entity]


#Best way

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]
