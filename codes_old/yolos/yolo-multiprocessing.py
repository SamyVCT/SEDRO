import cv2 as cv
import numpy as np
import time
from ultralytics import YOLO
import math 
import multiprocessing
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

def process_frames(frames, num_cores):
    with multiprocessing.Pool(processes=num_cores) as pool:  
        results = pool.map(detect_objects, frames)
    return results


def display_realtime_results(output_frame):
    cv.namedWindow('Object Detection', cv.WINDOW_NORMAL)
    while True:
        if not output_frame.empty():
            frames, detected_objects = output_frame.get()
            for frame, objs in zip(frames, detected_objects):
                for obj in objs:
                    # Draw detected objects on the frame
                    cv.rectangle(frame, (obj['x1'], obj['y1']), (obj['x2'], obj['y2']), (0, 255, 0), 2)
                    cv.putText(frame, obj['label'], (obj['x1'], obj['y1'] - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Display the frame with detected objects in real-time
                cv.imshow('Object Detection', frame)
                if cv.waitKey(1) == ord('q'):
                    break
def main():
    cap = cv.VideoCapture(0)  # Initialize your webcam or video source
    output_frame = multiprocessing.Queue()

    process = multiprocessing.Process(target=display_realtime_results, args=(output_frame,))
    process.start()
    num_cores = 8
    frames = []
    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            break
        frames.append(frame)

        if len(frames) >= 1:  # Process frames in batches of 4
            detected_objects = process_frames(frames, num_cores)
            output_frame.put((frames, detected_objects))
            frames = []

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
