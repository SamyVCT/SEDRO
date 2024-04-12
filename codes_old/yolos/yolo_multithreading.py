import cv2 as cv
import numpy as np
import time
from ultralytics import YOLO
import math 
import threading
import os

model = YOLO("yolo-Weights/yolov8n.pt")
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
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

def detect_objects(img):
    # Your YOLOv8 object detection code here for a single frame
    # Perform object detection on the frame
    # Return the detected objects
    detected_objects = []  # Placeholder for detected objects

    results = model(img, stream=True, imgsz=1920)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            cls = int(box.cls[0])
            dict = {}
            dict['label'] = classNames[cls]
            dict['x1'] = int(x1)
            dict['y1'] = int(y1)
            dict['x2'] = int(x2)
            dict['y2'] = int(y2)
            detected_objects.append(dict)

    return detected_objects


def display_realtime_results(cap):
    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            break

        frames_to_process = [frame]  # Add frames to this list

        # Divide frames into chunks for multiprocessing
        detected_objects = detect_objects(frame)

        
        # Display the frames with detected objects in real-time
        for obj in detected_objects:
            # print(detected_objects)
            # print("hello")
            # Assuming obj contains coordinates or information to draw bounding boxes
            cv.rectangle(frame, (int(obj['x1']), int(obj['y1'])), (int(obj['x2']), int(obj['y2'])), (0, 255, 0), 2)
            cv.putText(frame, obj['label'], (int(obj['x1']), int(obj['y1']) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Display the frame with detected objects in real-time
        cv.imshow('Object Detection', frame)
        
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

cap = cv.VideoCapture(0)  # Initialize your webcam or video source
display_thread = threading.Thread(target=display_realtime_results, args=(cap,))
display_thread.start()
display_thread.join()
