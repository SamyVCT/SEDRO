# -*- coding: utf-8 -*-
'''
Ce programme utilise la bibliothèque OpenCV pour détecter et tracer un cercle autour d'objets 
qui correspondent à une certaine plage de couleurs spécifiée. Il commence par définir la plage
de couleurs à détecter en termes de limites inférieures et supérieures dans l'espace de couleur
HSV, puis convertit une image donnée en espace de couleur HSV et applique un flou pour réduire
le bruit. Ensuite, il crée un masque pour filtrer tous les pixels de l'image qui ne correspondent
pas à la plage de couleurs spécifiée. Le programme trouve les contours des objets dans le masque 
filtré et trace un cercle autour de l'objet avec le plus grand contour (supposé être l'objet recherché).
Finalement, l'image d'origine avec le cercle tracé est affichée.
'''
#import des bibliothèques nécessaires
import cv2
import numpy as np

def p2(img):

    #4 lignes permettant de trouver les composantes H,S,V à partir des composantes B,G,R 
    #Par exemple le bleu (foncé) correspond au triplet [120,255,255]
    pixel = np.array([[[255, 0, 0]]]) #attention BVR et pas RVB en python
    pixel = pixel.astype(np.uint8)
    couleur = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)

    # définition des bornes hautes et basses de couleur low et high
    # définition de la couleur d'écriture color_infos
    # les variables low2 et high2 sont utilisées pour le détection de couleur rouge
    # car dans l'espace HSV le rouge se situe au début du cercle (0-10) et à la fin (245-255)
    # mask2 et bitwise_or sont aussi utilisées pour le rouge
    # low = np.array([100,120,70])
    # high = np.array([130,255,255])
    low = np.array([245, 50, 150])
    high = np.array([255, 255, 255])
    color_infos = (0,255,255)

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
    
    #cv2.imshow('Camera', img)
    #cv2.imshow('Image2', img2)
    #cv2.imshow('Mask', mask)
    cv2.imshow('image',img_hsv)
    cv2.waitKey(0)
    

p2(cv2.imread("C:/Users/samyv/OneDrive/Documents/ensta cours/2a/pie/SEDRO/codes/yolos/images/image_tennis.jpg"))
