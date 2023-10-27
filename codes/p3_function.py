# -*- coding: utf-8 -*-
"""
Le programme prend une image en entrée, la convertit en image YUV, puis la floute et 
la divise en trois canaux de couleurs : Y, U et V. Les canaux U et V sont convertis en
images en niveaux de gris, puis sont chacun transformés à l'aide de tables de correspondance
de couleur (LUT) pour créer des images YUV. Le programme utilise ensuite un seuillage pour
isoler les pixels de l'image V qui ont une valeur comprise entre 127 et 128, puis applique
des opérations d'érosion et de dilatation pour éliminer les petits artefacts. Enfin, le programme
trouve le plus grand contour de l'image seuillée et dessine un rectangle autour de celui-ci sur
l'image d'entrée. Le résultat final est affiché dans une fenêtre de sortie en temps réel.
"""

import cv2
import numpy as np

#création de bandes de couleurs pour convertir les images en gris en images Y,U,V car Python bugue avec les images Y,U,V
def make_lut_u():
    return np.array([[[i,255-i,0] for i in range(256)]],dtype=np.uint8)

def make_lut_v():
    return np.array([[[0,255-i,i] for i in range(256)]],dtype=np.uint8)

def p3(img):
    lut_u, lut_v = make_lut_u(), make_lut_v()

    low = np.array([0,127,127]) #attention BVR et pas RVB en python
    high = np.array([1,128,128])
    color_infos = (0,255,255)
    #cap = cv2.VideoCapture("vidéo.mp4")
    #cap = cv2.VideoCapture(0)


    #ret, img = cap.read()
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv = cv2.blur(img_yuv, (5,5))
    y, u, v = cv2.split(img_yuv)
    y = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
    u = cv2.cvtColor(u, cv2.COLOR_GRAY2BGR)
    v = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)
    u_mapped = cv2.LUT(u, lut_u)
    v_mapped = cv2.LUT(v, lut_v)
    mask_v = cv2.inRange(v_mapped, low, high)
    mask_v = cv2.erode(mask_v, None, iterations = 4)
    mask_v = cv2.dilate(mask_v, None, iterations = 4)
    img2 = cv2.bitwise_and(v, v, mask = mask_v)
    elements = cv2.findContours(mask_v, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(elements) > 0:
        c = max(elements, key = cv2.contourArea)
        ((x,y), rayon) = cv2.minEnclosingCircle(c)
        cv2.rectangle(img, (int(x-20), int(y-20)), (int(x+20),int(y+20)), color_infos, 1)
    cv2.imshow('Camera', img)
    cv2.imshow("u",u_mapped)
    cv2.imshow("v",v_mapped)
    #cv2.imshow("mask_v",mask_v)
    cv2.waitKey(0)

p3(cv2.imread("C:/Users/samyv/OneDrive/Documents/ensta cours/2a/pie/SEDRO/codes/yolos/images/image_tennis.jpg"))

            