import cv2 
import numpy as np 


def extract_color(cap, mask_low, mask_high):
	ret,frame =cap.read() 
	# ret will return a true value if the frame exists otherwise False 
	into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
	# changing the color format from BGr to HSV 
	# This will be used to create the mask 
	L_limit=np.array(mask_low) # [98,50,50] setting the blue lower limit / [0,50,50] red / 
	U_limit=np.array(mask_high) # [139,255,255] setting the blue upper limit / [40,255,255] red / 
	
		

	b_mask=cv2.inRange(into_hsv,L_limit,U_limit) 
	# creating the mask using inRange() function 
	# this will produce an image where the color of the objects 
	# falling in the range will turn white and rest will be black 
	blue=cv2.bitwise_and(frame,frame,mask=b_mask) 
	# this will give the color to mask. 

	global out
	out = blue

