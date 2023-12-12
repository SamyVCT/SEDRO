import cv2

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
    

def updateCameras(menuCamera):
    menuCamera.delete(0, 'end')
    menuCamera.add_command(label="Update", command=lambda: updateCameras())
    for i in range(0, 5):
        cam = cv2.VideoCapture(i)
        if cam.isOpened():
            menuCamera.add_command(label="Camera " + str(i), command=lambda c=i:changeCamera(c))
        cam.release()