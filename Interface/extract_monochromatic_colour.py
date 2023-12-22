import cv2 
import numpy as np 
from multiprocessing import Manager

# This program is used both to extract a color from the image and to retrieve the image in real time for all processes
# Ce programme sert à la fois à extraire une couleur de l'image et à récupérer l'image en temps réel pour tous les processus
def extract_color(cap, mask_low, mask_high, globImage):
	try:
		ret,frame =cap.read() 

		# Make the image global to all processes
		# Rend l'image globale à tous les processus
		if(len(globImage) == 0):
			globImage.append(frame)
			globImage.append(frame)
		globImage[0] = frame

		# Convert the image to HSV
		# Convertit l'image en HSV
		into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
		
		# This will be used to create the mask
		L_limit=np.array(mask_low) # [98,50,50] setting the blue lower limit / [0,50,50] red / 
		U_limit=np.array(mask_high) # [139,255,255] setting the blue upper limit / [40,255,255] red / 
		
			
		b_mask=cv2.inRange(into_hsv,L_limit,U_limit) 
		# creating the mask using inRange() function 
		# this will produce an image where the color of the objects 
		# falling in the range will turn white and rest will be black 


		filtered_frame=cv2.bitwise_and(frame,frame,mask=b_mask) 
		# this will give the color to mask.

		return filtered_frame
	except:
		pass

