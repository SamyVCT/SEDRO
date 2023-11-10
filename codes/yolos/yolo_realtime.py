import cv2 as cv
from cv2.dnn import NMSBoxes
import numpy as np
import time
'''
Ce programme utilise la bibliothèque OpenCV pour effectuer la détection d'objets en temps réel sur une vidéo 
à l'aide de YOLOv8 (You Only Look Once version 8). Tout d'abord, il charge les noms de classes 
et attribue des couleurs aléatoires à chacune d'elles. Ensuite, il charge les fichiers de configuration 
et de poids du modèle YOLOv8, crée un objet réseau et définit les couches de sortie. La fonction 
"yolo_function" est définie pour effectuer la détection d'objets sur une image donnée. Cette fonction
prend une image en entrée et retourne une image avec des boîtes englobantes autour des objets détectés
avec une probabilité de détection supérieure à 50%. Les boîtes englobantes sont accompagnées d'étiquettes
indiquant le nom de la classe et la probabilité de détection. Enfin, le programme affiche l'image résultante
avec les boîtes englobantes et les étiquettes.
'''
from ultralytics import YOLO
import math 
# start webcam
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
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


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv.imshow('Webcam', img)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

