
from datetime import datetime
from threading import Thread

from ultralytics import YOLO
import cv2
import math

from models.detection import Detection
from upload_image import create_image
from yolov8_detect_video import get_detection


def upload_and_save_detection(image_to_upload, filename):
    try:
        image_url = create_image(image_to_upload.tobytes())
        detect = Detection(
            name=filename,
            date=datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"),
            image=image_url,
            description="",
            detections=[],
        )
        get_detection(detect)  # Upload and save detection data
        print(f"Image uploaded and detection saved successfully for: {filename}")
    except Exception as e:
        print(f"Error uploading image for {filename}: {e}")


cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Model path (replace with your weights path)
model = YOLO("weights/best3.pt")

classNames = ['Garbage_Bag', 'Glass', 'Paper_Bag', 'Pet_Bottle', 'Plastic_Bag', 'can']

start_time = datetime.now()
detection_interval = 10
has_detection = False

while True:
    success, img = cap.read()
    if not success:
        continue

    # Object detection using YOLOv8
    results = model.predict(img, stream=True)

    # Process detections and draw bounding boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Draw bounding box and label
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            class_name = classNames[cls]
            label = f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            has_detection = True

    # Calculate elapsed time only once per frame
    elapsed_time = (datetime.now() - start_time).total_seconds()

    # Save image logic (if object detected)
    if has_detection:
        if elapsed_time >= detection_interval:
            # Reset timer and flag for next interval
            start_time = datetime.now()
            has_detection = False

            # Generate filename with formatted date and time
            filename = f"Detection_{start_time.strftime('%a, %d %b %Y %H:%M:%S')}"
            ret, image_to_upload = cv2.imencode(".jpg", img)

            # Create a separate thread for image upload and saving
            upload_thread = Thread(target=upload_and_save_detection, args=(image_to_upload, filename))
            upload_thread.start()

    # Display the frame
    cv2.imshow("Webcam detection", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()