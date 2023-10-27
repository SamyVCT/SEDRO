# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:31:29 2022

@author: Gaëtan Le Fournis
"""

#import des bibliothèques nécessaires
import numpy as np
import pandas as pd
import cv2

#lecture de l'image qui se trouve dans le même dossier que le programme
img = cv2.imread("logo.jpg")
(hauteur, largeur, epaisseur) = img.shape

#import du document csv contenant 865 couleurs R,G,B
index = ["couleur", "nom_couleur", "code_hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None, sep=";")
l = len(csv)

#Initialisation des variables
clicked = False
r = g = b = xpos = ypos = 0

#fonction couleur qui renvoie la couleur d'un pixel à partir de ces composantes R,G,B
def couleur(R,G,B):
    minimum = 100000
    #calcul de la distance entre le pixel et chaque couleur du doc csv
    for i in range(l):
        d = abs(R - int(csv.loc[i,"R"])) + abs(G - int(csv.loc[i,"G"]))+ abs(B - int(csv.loc[i,"B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i,"nom_couleur"]
    return cname

#fonction qui permet à un événement de déclencher quelque chose.
#Ici, l'événement est un double clic gauche de la souris et permet de
#changer clicked en "True" tout en gardant en mémoire les composantes R,G,B du pixel
def clic_souris(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        
#Boucle infinie tant qu'on appuie pas sur 'q''
while(True):
    #création de la fenêtre (nom, dimension,fenêtre sur laquelle clic_souris est effectué...)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image',largeur,hauteur)
    cv2.setMouseCallback('image', clic_souris)
    cv2.imshow('image',img)
    if (clicked):   
        #cv2.rectangle(image, point de départ, point d'arrivée, couleur, épaisseur (-1) pour remplir le rectangle entier
        cv2.rectangle(img,(20,20), (800,80), (b,g,r), -1)
        #crée un texte 
        text = couleur(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        if(r + g + b >= 600): #écriture en blanc ou noir en fonction de si la couleur est claire ou foncée
            #cv2.putText(image,texte,départ,arrivée,police,taille,couleur,épaisseur,type de ligne)
            cv2.putText(img, text,(50,66),2,1.1,(0,0,0),2,cv2.LINE_AA)
        else :
            cv2.putText(img, text,(50,66),2,1.1,(255,255,255),2,cv2.LINE_AA)
            
        clicked=False
    #arrêt de la boucle avec la touche 'q'    
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()










