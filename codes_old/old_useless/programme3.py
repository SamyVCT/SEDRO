# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 22:35:31 2022

@author: Gaëtan Le Fournis
"""


import cv2
import numpy as np

#création de bandes de couleurs pour convertir les images en gris en images Y,U,V car Python bugue avec les images Y,U,V
def make_lut_u():
    return np.array([[[i,255-i,0] for i in range(256)]],dtype=np.uint8)

def make_lut_v():
    return np.array([[[0,255-i,i] for i in range(256)]],dtype=np.uint8)

lut_u, lut_v = make_lut_u(), make_lut_v()

low = np.array([0,127,127]) #attention BVR et pas RVB en python
high = np.array([1,128,128])
color_infos = (0,255,255)
cap = cv2.VideoCapture("vidéo.mp4")
#cap = cv2.VideoCapture(0)


while True:
    ret, img = cap.read()
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
    cv2.imshow("mask_v",mask_v)
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()


        