##################### Auteurs:  #####################
# - LACHEVRE Corentin                               #
# - VINCENT Samy                                    #
# - HENRIQUE MARQUES GONCALVES Luiz                 #
#####################################################

from PIL import Image, ImageDraw, ImageTk
import math
import tkinter as tk
from tkinter import colorchooser
from threading import Thread
from threading import Lock
from multiprocessing import Process
from multiprocessing import Manager
import time
import imageio
import sys
import colorsys

import yolo_realtime
import cameraChooser
import extract_monochromatic_colour
import cv2
from math import floor

import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./Images/")

    return os.path.join(base_path, relative_path)


##############################################################################################################
# Partie purement graphique de l'interface                                                                   #
##############################################################################################################

def printDetectionList(panel):
    T = tk.Text(panel, font=("Arial", 15), bg="#303030", fg="white",highlightthickness=0)
    T.pack()
    while True:
        # Clear the text in the panel
        T.delete('1.0', tk.END)
        try:
            detectionList = globImage[2]
        except:
            detectionList = None
        if detectionList is not None:
            while len(detectionList) > 15:
                detectionList.pop(0)
                globImage[2].pop(0)
            for detection in reversed(detectionList):
                T.insert(tk.END, f"{detection}\n")
        time.sleep(0.5)

# Retourne les dimensions de l'écran
def getScreenSize():
    largura = root.winfo_screenwidth()
    altura = root.winfo_screenheight()
    return largura, altura

# Transforme les frames de la caméra en images tkinter
def get_frame(video):
    try:
        frame_dimensionned = Image.fromarray(cv2.cvtColor(video, cv2.COLOR_BGR2RGB)).resize(video_size).convert('RGBA')
        return ImageTk.PhotoImage(frame_dimensionned)
  
    except Exception as e:
        print(e)
        return None
    
def click(event, panelClicked):
    # Récuperer les coordonnées du clic
    x, y = event.x, event.y

    global third_size
    global video_size
    global map_size

    third_size = getScreenSize()
    video_size = getScreenSize()
    map_size = getScreenSize()

    mapPanel.place_forget()
    yoloPanel.place_forget()
    colorPanel.place_forget()

    panelClicked.place(x = 0, y = 0)

# Retourne toutes les fenêtres à la normale
def return_images():
    global map_size
    global video_size
    global third_size
    map_size = (int(700*width/1536), int(350*height/864))
    video_size = (int(700*width/1536), int(350*height/864))
    third_size = (int(700*width/1536), int(350*height/864))
    mapPanel.place(x=root.winfo_screenwidth() - 750*width/1536, y=20*height/864)
    yoloPanel.place(y=root.winfo_screenheight() - 460*height/864, x=root.winfo_screenwidth() - 750*width/1536)
    colorPanel.place(y=root.winfo_screenheight() - 460*height/864, x=25*width/864)


##############################################################################################################
# Partie purement fonctionnelle de l'interface                                                               #
##############################################################################################################


# Boucle while récupérant et affichant les images de la caméra traitées par yolo
def yoloVideoPlayer(mapPanel):
    while True:
        # print('in here')
        try:
            frame = get_frame(globImage[1])
        except:
            frame = None
        if frame is not None:
            mapPanel.configure(image=frame)
            mapPanel.image = frame

# Boucle while affichant les images de la caméra avec le filtre de couleur
def colorVideoPlayer(mapPanel):
       while True:
        # print('in here')
        try:
            frame = get_frame(extract_monochromatic_colour.extract_color(cameraChooser.cap, mask_low, mask_high, globImage))
        except:
            frame = None
        if frame is not None:
            mapPanel.configure(image=frame)
            mapPanel.image = frame


def colorChoice(color): #3-array RGB
    colorMin = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255)
    global mask_low
    global mask_high
    mask_low = [0,0,0]
    mask_high = [0,0,0]

    mask_low = [max(floor((colorMin[0])*255 - 10), 0), 5, 5]

    if color != [255,255,255]:
        colorMaxBrut = colorchooser.askcolor(title="Choisir la couleur maximale")[0]
    else:
        colorMaxBrut = color
    colorMax = colorsys.rgb_to_hls(colorMaxBrut[0]/255, colorMaxBrut[1]/255, colorMaxBrut[2]/255)
    #mask_low = [max(floor((colorHSV[0])*255 - 40), 0), max(floor((colorHSV[1])*255 - 100), 0), max(floor((colorHSV[2])*255 - 100), 0)]
    mask_high = [min(floor(colorMax[0]*255 + 10), 255), min(floor(colorMax[1]*255 + 20), 255), min(floor(colorMax[2]*255 + 20), 255)]

    #Show color on the button
    colorList = (math.floor(color[0]), math.floor(color[1]), math.floor(color[2]))
    buttonColor = "#%02x%02x%02x" % colorList
    colorButton.configure(bg=buttonColor)


##############################################################################################################
#                                Partie principale de l'interface                                            #
##############################################################################################################

if __name__ == "__main__":  # confirms that the code is under main function
    # Créer la fenetre principale
    root = tk.Tk()
    root.title("SEDRO")
    root.state("zoomed")
    width, height = getScreenSize()


    map_size = (int(700*width/1536), int(350*height/864))
    video_size = (int(700*width/1536), int(350*height/864))
    third_size = (int(700*width/1536), int(350*height/864))


    root.geometry(f"{width}x{height}")
    root.configure(bg="#303030")

    mapPanel = tk.Label(root,highlightthickness=0)

    img = Image.open(resource_path("loading.png")).convert('RGBA')
    img_tk = ImageTk.PhotoImage(img)
    # mapPanel = tk.Label(root, image = img_tk)
    #yoloPanel = tk.Label(root, image = img_tk, text="Le chargement peut être long,      \n veuillez patienter.", compound=tk.RIGHT, font=("Arial", 15), bg="#303030", fg="white")
    yoloPanel = tk.Label(root, image = img_tk, compound=tk.RIGHT, font=("Arial", 15), bg="#303030", fg="white")
    colorPanel = tk.Label(root, image = img_tk)

    mapPanel.bind("<Button-1>", lambda e: click(e, mapPanel)) # <Button-1> est le clic gauche de la souris
    yoloPanel.bind("<Button-1>", lambda e: click(e, yoloPanel)) 
    colorPanel.bind("<Button-1>", lambda e: click(e, colorPanel))

    mapPanel.bind("<Enter>", lambda e: mapPanel.config(cursor="hand2"))  # "hand2" est un curseur de main
    mapPanel.bind("<Leave>", lambda e: mapPanel.config(cursor=""))

    yoloPanel.bind("<Enter>", lambda e: yoloPanel.config(cursor="hand2"))  # "hand2" est un curseur de main
    yoloPanel.bind("<Leave>", lambda e: yoloPanel.config(cursor=""))

    colorPanel.bind("<Enter>", lambda e: colorPanel.config(cursor="hand2"))  # "hand2" est un curseur de main
    colorPanel.bind("<Leave>", lambda e: colorPanel.config(cursor=""))

    root.bind("<Escape>", lambda e: return_images())

    mapPanel.place(x=root.winfo_screenwidth() - 750*width/1536, y=20*height/864)
    yoloPanel.place(y=root.winfo_screenheight() - 460*height/864, x=root.winfo_screenwidth() - 750*width/1536)
    colorPanel.place(y=root.winfo_screenheight() - 460*height/864, x=25*width/864)


    # List of cameras menu
    zoneMenu = tk.Frame(root, borderwidth=3, bg='#557788')
    zoneMenu.grid(row=0,column=0)
    menuDerCameras = tk.Menubutton(zoneMenu, text="Cameras")
    menuDerCameras.grid(row=0,column=0)

    menuCamera = tk.Menu(menuDerCameras)
    cameraChooser.updateCameras(menuCamera)
    cameraChooser.init()
    menuDerCameras.config(menu=menuCamera)
    # Button to choose color
    colorButton = tk.Button(zoneMenu, text='Changer couleur', command=lambda: colorChoice(colorchooser.askcolor(title="Choisir une couleur minimale à détecter")[0]))
    colorButton.grid(row=0,column=1)


    colorChoice([255,255,255])

    # Lancement des differents threads et processus : parallélisation des tâches
    # threadMap = Thread(target=MapLoop, args=(mapPanel, img))
    threadDetectionList = Thread(target=printDetectionList, args=(mapPanel,))
    threadVideoYolo = Thread(target=yoloVideoPlayer, args=(yoloPanel,))
    threadVideoColor = Thread(target=colorVideoPlayer, args=(colorPanel,))

    # threadMap.daemon = True 
    threadDetectionList.daemon = True
    threadVideoColor.daemon = True 
    threadVideoYolo.daemon = True

    globImage = Manager().list() # Mémoire partagée entre les processus
    processYolo = Process(target=yolo_realtime.yolo_realtime_boot, args=(globImage,))

    # Lancement des processus et threads
    processYolo.start()
    threadVideoColor.start()
    threadDetectionList.start()
    # threadMap.start()
    threadVideoYolo.start()


    # Intialiser la boucle principale
    root.mainloop()

    cameraChooser.cap.release()
    cv2.destroyAllWindows() 