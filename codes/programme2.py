# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 15:21:40 2022

@author: Gaëtan Le Fournis
"""

#import des bibliothèques nécessaires
import cv2
import numpy as np

#4 lignes permettant de trouver les composantes H,S,V à partir des composantes B,G,R 
#Par exemple le bleu (foncé) correspond au triplet [120,255,255]
pixel = np.array([[[255, 0, 0]]]) #attention BVR et pas RVB en python
pixel = pixel.astype(np.uint8)
couleur = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
print(couleur[0][0])

# définition des bornes hautes et basses de couleur low et high
# définition de la couleur d'écriture color_infos
# les variables low2 et high2 sont utilisées pour le détection de couleur rouge
# car dans l'espace HSV le rouge se situe au début du cercle (0-10) et à la fin (245-255)
# mask2 et bitwise_or sont aussi utilisées pour le rouge
low = np.array([100,120,70])
high = np.array([130,255,255])
# low2 = np.array([245, 50, 150])
# high2 = np.array([255, 255, 255])
color_infos = (0,255,255)

# permet de lire soit une vidéo soit la webcam de l'ordinateur (0)

#cap = cv2.VideoCapture("DJI_0270.mp4")
cap = cv2.VideoCapture(0)

#lecture de la vidéo en continue
while True:
    ret, img = cap.read()
    #convertir la couleur B,G,R en H,S,V
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #effectuer un floutage par des convolutions de noyaux de taille 5
    img_hsv = cv2.blur(img_hsv, (5,5))
    
    
    #création de mask pour faire ressortir seulement ce qui nous intéresse
    mask = cv2.inRange(img_hsv, low, high)
    # mask2 = cv2.inRange(frame, low2, high2)
    mask = cv2.erode(mask, None, iterations = 3)
    mask = cv2.dilate(mask, None, iterations = 3)
    
    
    #renvoie l'image de base avec seulement les objets intéressants
    # inter = cv2.bitwise_or(mask, mask2)
    img2 = cv2.bitwise_and(img, img, mask = mask)
    #trouve le contour des objets importants
    elements = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
          
    if len(elements) > 0:
        c = max(elements, key = cv2.contourArea)
        #trouve le cercle le plus petit contenant l'élément
        ((x,y), rayon) = cv2.minEnclosingCircle(c)
        #dessine un cercle sur l'image de base pour mieux repérer l'objet détecté
        cv2.circle(img, (int(x), int(y)), int(rayon), color_infos, 2)
    cv2.imshow('Camera', img)
    cv2.imshow('Image2', img2)
    #cv2.imshow('Mask', mask)
    #cv2.imshow('image',img_hsv)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
        
