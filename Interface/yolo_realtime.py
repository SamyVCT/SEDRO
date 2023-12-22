import cv2 as cv
from cv2.dnn import NMSBoxes
import numpy as np
import time
import os
import extract_monochromatic_colour
from multiprocessing import Manager
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
import cameraChooser
import math 

# start webcam
def yolo_realtime_boot(globImage):


    # model
    model = YOLO("yolo-Weights/yolov8n.pt")
    #model.to('cuda') # uncomment this line if you want to use GPU - needs CUDA to be installed on your system 
    #os.environ["CUDA_VISIBLE_DEVICES"] = "-1" #uncomment to force the use of CPU (once you installed cuda for pytorch, it keeps using it by default)
    # pip3 install torchvision==0.16.0+cu121 -f https://download.pytorch.org/whl/torch_stable.html
    # pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 
    # Si ça marche pas peut être il faut installer CUDA 12.1 : https://developer.nvidia.com/cuda-toolkit

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
        # Get image from other process manager globImage
        # Récupère l'image depuis le processus manager globImage
        if(len(globImage) == 0):
            print("No image found")
            continue
        img = globImage[0]
        
        # Perform object detection on the frame. imgsz is the size at which the image is fed to the model.
        results = model(img, stream=True, imgsz=640)
        
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

                cv.putText(img, classNames[cls] + " confiance : " + str(confidence), org, font, fontScale, color, thickness)
        globImage[1] = img


