import cv2

# start webcam
def init():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)

def changeCamera(i):
    global cap
    cap.release()
    cap = cv2.VideoCapture(i)
    cap.set(3, 1920)
    cap.set(4, 1080)
    
# Mise à jour des caméras disponibles pour pouvoir choisir une caméra branchée après le lancement du programme
def updateCameras(menuCamera):
    menuCamera.delete(0, 'end')
    menuCamera.add_command(label="Update", command=lambda: updateCameras())
    # Suppose qu'il n'y a pas plus de 5 caméras branchées
    for i in range(0, 5):
        try:
            cam = cv2.VideoCapture(i)
        except:
            continue
        if cam.isOpened():
            menuCamera.add_command(label="Camera " + str(i), command=lambda c=i:changeCamera(c))
        cam.release()