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


# def polygonDirection(angle1, angle2, width, height):
#     center = (width/2, height/2)

#     angle1 = angle1%360
#     angle2 = angle2%360
    
#     if(angle1 < 45 or angle1 >= 315):
#         point1 = (width,  height/2 - width*math.tan(angle1*math.pi/180)/2)

#     elif (angle1 < 135):
#         point1 = (width/2 + height/(2*math.tan(angle1*math.pi/180)), 0)

#     elif (angle1 < 225):
#         point1 = (0, height/2 - width*math.tan(math.pi - angle1*math.pi/180)/2)

#     elif (angle1 < 315):
#         point1 = (width/2 - height*(math.tan(3*math.pi/2 - angle1*math.pi/180))/2, height)

#     if(angle2 < 45 or angle2 >= 315):
#         point2 = (width, height/2 - width*math.tan(angle2*math.pi/180)/2)

#     elif (angle2 < 135):
#         point2 = (width/2 + height/(2*math.tan(angle2*math.pi/180)), 0)

#     elif (angle2 < 225):
#         point2 = (0, height/2 - width*math.tan(math.pi - angle2*math.pi/180)/2)

#     elif (angle2 < 315):
#         point2 = (width/2 - height*(math.tan(3*math.pi/2 - angle2*math.pi/180))/2, height)


#     point1 = (point1[0] + point1[0] - width/2, point1[1] + point1[1] - height/2)
#     point2 = (point2[0] + point2[0]- width/2, point2[1] + point2[1] - height/2)

#     return [(width/2, height/2), point1, point2]

# def drawMap(color, angles, points, areas,mapPanel):
#     im = Image.open(resource_path("basedrone2.png")).resize(map_size).convert('RGBA')
#     width, height = im.width, im.height
#     drone = Image.open(resource_path("drone.png")).resize((50,25)).convert('RGBA')
#     d = ImageDraw.Draw(im)
#     widthDrone, heightDrone = drone.size
#     #print(angles[0][0], angles[0][1])
    

#     for angle in angles:
#         d.polygon(polygonDirection(angle[0], angle[1], width, height), fill=color, outline=color)

#     for x in points:
#         tamanho_ponto = 10
#         d.line((x[0] - tamanho_ponto, x[1] - tamanho_ponto, x[0] + tamanho_ponto, x[1] + tamanho_ponto), fill=x[2], width=5)
#         d.line((x[0] + tamanho_ponto, x[1] - tamanho_ponto, x[0] - tamanho_ponto, x[1] + tamanho_ponto), fill=x[2],width=5)

#     for area in areas:
#         tamanho_ponto = area[2]
#         d.ellipse((area[0] - tamanho_ponto, area[1] - tamanho_ponto, area[0] + tamanho_ponto, area[1] + tamanho_ponto), fill=area[3])


#     # x_ponto = 3*width/4
#     # y_ponto = 3*height/4
#     # tamanho_ponto = 10
#     # d.line((x_ponto - tamanho_ponto, y_ponto - tamanho_ponto, x_ponto + tamanho_ponto, y_ponto + tamanho_ponto), fill='red', width=5)
#     # d.line((x_ponto + tamanho_ponto, y_ponto - tamanho_ponto, x_ponto - tamanho_ponto, y_ponto + tamanho_ponto), fill='red',width=5)

#     im.paste(drone, (int(width/2 - widthDrone/2), int(height/2 - heightDrone/2)))

#     photo = ImageTk.PhotoImage(im)

#     mapPanel.configure(image=photo)
#     mapPanel.image = photo

# def MapLoop(mapPanel, im):
#     a1 = 0
#     a2 = 20

#     a3 = 180
#     a4 = 200

#     x1 = 300
#     y1 = 100
#     x2 = 200
#     y2 = 300

#     while(1):
#         drawMap('green', [(a1,a2), (a3,a4)], [(x1,y1,'blue'), (x2,y2, 'yellow')], [(300, 500, 50, '#f3000faa')],mapPanel)
#         a1 += 1
#         a2 += 1
#         a3 += 1
#         a4 += 1

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