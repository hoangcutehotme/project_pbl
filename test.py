import cv2
import torch
import numpy as np
# from deep_sort_realtime.deepsort_tracker import DeepSort
# from models.common import DetectMultiBackend, AutoShape
from ultralytics import YOLO
# from roboflow import Roboflow
# rf = Roboflow(api_key="WIFZhGRTt1WDUs9vLS9k")
# project = rf.workspace("hoang-nguyen-trong").project("littering-detect")
# version = project.version(1)
# dataset = version.download("yolov8")
# model = DetectMultiBackend(weights='best_train7.pt',device=device,)

# Config value
# video_path = "data_ext/highway.mp4"
conf_threshold = 0.5
tracking_class = None # None # None: track all

# Khởi tạo DeepSort sau 30 lan track ma ko thay vat the thi xoa
tracker = DeepSort(max_age=30)

# Khởi tạo YOLOv9
device = "mps:0" # "cuda": GPU, "cpu": CPU, "mps:0"
model = YOLO('')
model = AutoShape(model)


# Load classname từ file classes.names
with open("data_ext/classes_trash.names") as f:
    class_names = f.read().strip().split('\n')

colors = np.random.randint(0,255, size=(len(class_names),3 ))
tracks = []

# Khởi tạo VideoCapture để đọc từ file video
cap = cv2.VideoCapture(0)

# Tiến hành đọc từng frame từ video
while True:
    # Đọc
    ret, frame = cap.read()
    if not ret:
        continue
    # Đưa qua model để detect
    frame = cv2.resize(frame, (1024, 800))  # Resize to a smaller size (example)
    # frame = cv2.cvtColor(frame, cv2.COLOR_)  # Convert to RGB if needed

    results = model(frame)

    detect = []
    for detect_object in results.pred[0]:
        label, confidence, bbox = detect_object[5], detect_object[4], detect_object[:4]
        x1, y1, x2, y2 = map(int, bbox)
        class_id = int(label)

        if tracking_class is None:
            if confidence < conf_threshold:
                continue
        else:
            if class_id != tracking_class or confidence < conf_threshold:
                continue

        detect.append([ [x1, y1, x2-x1, y2 - y1], confidence, class_id ])


    # Cập nhật, gán ID bằng DeepSort
    tracks = tracker.update_tracks(detect, frame=frame)

    # Vẽ lên màn hình các khung chữ nhật kèm ID
    for track in tracks:
        if track.is_confirmed():
            track_id = track.track_id

            # Lấy toạ độ, class_id để vẽ lên hình ảnh
            ltrb = track.to_ltrb()
            class_id = track.get_det_class()
            x1, y1, x2, y2 = map(int, ltrb)
            color = colors[class_id]
            B, G, R = map(int,color)

            label = "{}-{}".format(class_names[class_id], track_id)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (B, G, R), 2)
            cv2.rectangle(frame, (x1 - 1, y1 - 20), (x1 + len(label) * 12, y1), (B, G, R), -1)
            cv2.putText(frame, label, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Show hình ảnh lên màn hình
    cv2.imshow("Camera", frame)
    # Bấm Q thì thoát
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()