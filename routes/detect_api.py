import datetime
from bson import ObjectId
from flask import Flask, render_template, Response, jsonify, request, session, Blueprint
from pydantic import ValidationError
from ultralytics import YOLO

from models.detection import Detection
from config.db import client, collection
from schemas.schema_detection import serializeDict, serializeList

detect_api = Blueprint('detect_api', __name__)


@detect_api.route('/api/detection', methods=['GET'])
def find_all_detections():
    try:
        # Get page number from query string (default to 1)
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        # Find detections with limit and skip for pagination
        detections = collection.find().skip(skip).limit(limit)

        # # Return the list of detections and total count (optional)
        total_count = collection.count_documents({})
        return jsonify(
            {"limit": limit,
             "page": page,
             "total": total_count,
             "data": serializeList(detections),
             })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # return serializeList(collection.find())


@detect_api.get('/api/detection/<id>')
def find_one_user(id):
    try:
        return serializeDict(collection.find_one({"_id": ObjectId(id)}))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@detect_api.route('/api/detection', methods=['POST'])
def create_detection():
    try:
        raw_detection = request.get_json()
        time_now = datetime.datetime.now()
        raw_detection['date'] = time_now
        detect = Detection(**raw_detection)

        post_detect = collection.insert_one(detect.dict())
        the_detect = collection.find_one({"_id": post_detect.inserted_id})
        return jsonify({
            "status": "success",
            "data":
            serializeDict(the_detect)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@detect_api.route('/api/detection/<id>', methods=['PUT'])
def update_detection(id):
    try:
        # Validate detection data using Pydantic
        detect_data = request.get_json()
        detect = Detection(**detect_data)  # Raises ValidationError if invalid

        # Convert ID to ObjectId for MongoDB
        detection_id = ObjectId(id)

        # Update the document using the validated data
        updated_detection = collection.find_one_and_update(
            {"_id": detection_id},
            {"$set": dict(detect)}
        )

        if not updated_detection:
            return jsonify({"error": "Detection not found"}), 404

        # Return the updated detection (if found)
        return jsonify(updated_detection)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@detect_api.route('/api/detection/<id>', methods=['DELETE'])
def delete_detection(id):
    try:
        # Convert ID to ObjectId for MongoDB
        detection_id = ObjectId(id)

        # Delete the document and return the deleted detection (if found)
        deleted_detection = collection.find_one_and_delete({"_id": detection_id})

        if not deleted_detection:
            return jsonify({"error": "Detection not found"}), 404

        return jsonify(serializeDict(deleted_detection))
    except Exception as e:
        return jsonify({"error": str(e)}), 400
