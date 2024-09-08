import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    model = YOLO("../Yolo-Weights/yolov8l.pt")

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

    mask = cv2.imread("mask4.png")

    # Tracking
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    limits = [100, 297, 900, 297]
    totalCount = []

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.resize(img, (950, 480))
        imgRegion = cv2.bitwise_and(img, mask)
        #imgRegion=img

        imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, imgGraphics, (0, 0))
        results = model(imgRegion, stream=True)

        detections = np.empty((0, 5))

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                if currentClass == "car" or currentClass == "truck" or currentClass == "bus" \
                        or currentClass == "motorbike" and conf > 0.3:
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))

        resultsTracker = tracker.update(detections)

        for result in resultsTracker:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
                if totalCount.count(id) == 0:
                    totalCount.append(id)

    return len(totalCount)
