import datetime
from bson import ObjectId
from flask import Flask, render_template, Response, jsonify, request, session
#FlaskForm--> it is required to receive input from the user
# Whether uploading a video file  to our object app model
from flask_wtf import FlaskForm
from pydantic import ValidationError
from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os
from models.detection import Detection
from config.db import client, collection
from schemas.schema_detection import serializeDict, serializeList

# Required to run the YOLOv8 model
import cv2
from yolov8_detect_video import video_detection
from routes.webserver_route import webserver_route
from routes.detect_api import detect_api
from routes.process_api import process_api
# from pymongo import MongoClient

# # api for app
# from fastapi import FastAPI
# from routes.detetect_routes import app
#
# app_api = FastAPI()
# app_api.include_router(app)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hoangdev'
app.config['UPLOAD_FOLDER'] = 'static/files'

app.register_blueprint(webserver_route)
app.register_blueprint(detect_api)
app.register_blueprint(process_api)

@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    app.run(debug=True)
