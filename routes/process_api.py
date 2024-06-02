import cv2
from flask import Flask, render_template, Response, jsonify, request, session, Blueprint
from pydantic import ValidationError
from ultralytics import YOLO
from PIL import Image
import io
import numpy as np
import base64

from upload_image import create_image

process_api = Blueprint('process_api', __name__)
model = YOLO("weights/best4.pt")

# model = torch.hub.load("weights/best4.pt", 'yolov8n')


@process_api.route('/api/process_image', methods=['POST'])
def process_image():
    try:
        # Check if the image is in the request
        if 'image' not in request.files:
            return jsonify({"error": "Missing image data"}), 400

        image_file = request.files['files']

        # Read the image file and convert it to a format suitable for YOLO
        image = Image.open(io.BytesIO(image_file.read())).convert('RGB')

        img = np.array(image)

        # Perform YOLO detection
        results = model.predict(img,conf=0.25,iou=0.7)

        # Render results and get the annotated image
        annotated_img = results[0].plot()  # This should work with YOLOv8

        # Convert the annotated image to bytes
        _, encoded_img = cv2.imencode('.jpg', annotated_img)
        encoded_img_bytes = encoded_img.tobytes()

        image_url = create_image(io.BytesIO(encoded_img_bytes))

        return jsonify({
            "status": "success",
            "processed_image": image_url  # Base64 encoded string
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
