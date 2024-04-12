import cv2 as cv
from cv2.dnn import NMSBoxes
import numpy as np
import time
'''
Ce programme utilise la bibliothèque OpenCV pour effectuer la détection d'objets dans une image 
à l'aide de YOLOv3 (You Only Look Once version 3). Tout d'abord, il charge les noms de classes 
et attribue des couleurs aléatoires à chacune d'elles. Ensuite, il charge les fichiers de configuration 
et de poids du modèle YOLOv3, crée un objet réseau et définit les couches de sortie. La fonction 
"yolo_function" est définie pour effectuer la détection d'objets sur une image donnée. Cette fonction
prend une image en entrée et retourne une image avec des boîtes englobantes autour des objets détectés
avec une probabilité de détection supérieure à 50%. Les boîtes englobantes sont accompagnées d'étiquettes
indiquant le nom de la classe et la probabilité de détection. Enfin, le programme affiche l'image résultante
avec les boîtes englobantes et les étiquettes.
'''

# Load names of classes and get random colors
classes = open('C:/Users/samyv/OneDrive/Documents/ensta cours/2a/pie/SEDRO/codes/yolos/coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

# Donne le fichier de config et le fichier avec les poids pour le modèle puis charge le réseau
net = cv.dnn.readNetFromDarknet('C:/Users/samyv/OneDrive/Documents/ensta cours/2a/pie/SEDRO/codes/yolos/yolov3.cfg', 'C:/Users/samyv/OneDrive/Documents/ensta cours/2a/pie/SEDRO/codes/yolos/yolov3.weights')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)

# couche de sortie 
ln = net.getLayerNames()
try:
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
except IndexError:
    # si get...Layers retourne tableau 1D when CUDA isn't available
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


def yolo_function(img):
    t0 = time.time()

    #contruction du blob à partir de l'image 
    blob = cv.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)

    #On donne l'objet blob en entrée du réseau + calcul du temps 
    net.setInput(blob)
    outputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []
    h, w = img.shape[:2]

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.5:
                box = detection[:4] * np.array([w, h, w, h])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                box = [x, y, int(width), int(height)]
                boxes.append(box)
                confidences.append(float(confidence))
                classIDs.append(classID)

    # Desenhe apenas as detecções com mais de 50% de confiança
    indices = cv.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
    for i in indices:
        (x, y, w, h) = boxes[i]
        color = [int(c) for c in colors[classIDs[i]]]
        cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
        cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    t1 = time.time()
    print('time=', t1-t0)

    cv.imshow('window', img)
    cv.waitKey(0)
    #cv.destroyAllWindows()

yolo_function(cv.imread("C:/Users/samyv/OneDrive/Documents/ensta cours/2a/pie/SEDRO/codes/yolos/images/image1.jpg"))