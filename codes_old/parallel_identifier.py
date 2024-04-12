import cv2
from mpi4py import MPI
import numpy as np
from p3_function import p3
from p2_function import p2
from yolo_chloe.yolo import yolo_function

'''
Le logiciel utilise la bibliothèque OpenCV pour capturer des images à partir 
d'une caméra et les traiter en utilisant différents programmes sur plusieurs 
processeurs, à l'aide de OpenMPI. Le programme principal s'exécute sur le processus 0,
où il capture les images, les redimensionne et les envoie à tous les autres processus.
Les autres processus, chacun exécutant un programme différent, reçoivent les images, les
transforment en un tableau numpy et effectuent leur propre traitement spécifique au programme.
Les différents programmes inclus sont p2_function.py, p3_function.py et yolo.py. 
Le processus 1 utilise le programme p2_function.py, le processus 2 utilise le programme p3_function.py
et le processus 3 utilise le programme yolo.py. Les processus s'exécutent indéfiniment jusqu'à ce qu'une 
touche soit pressée pour fermer le programme. (ctrl C)
'''

# MPI initialization
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # rank of the current process
size = comm.Get_size()  # total number of processes

if rank == 0:
    FILE = "../video.MP4"
    cap = cv2.VideoCapture(FILE)

    # read the first frame of the video
    ret, first_frame = cap.read()

    while True:
        # read the current frame of the video
        ret, frame = cap.read()
        # resize the frame
        frame = cv2.resize(frame, (600, 500))

        # check if the frame is empty
        if not ret:
            break

        # encode the frame as a jpeg image
        img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        img_size = len(img_bytes)

        # send the image to other processes
        for proc in range(1, size):
            # send data size to other processes
            comm.send(img_size, dest=proc, tag=0)
            # send the image to other processes
            comm.send(img_bytes, dest=proc, tag=1)

        # show the current frame
        cv2.imshow('process 0', frame)

        #uncomment the next line to make yolo_function in the first processor:
        #yolo_function(frame)


        # check for the 'q' key pressed, to quit the program
        if cv2.waitKey(1) & (0xFF == ord('q')):
            break

    # destroy all windows and release the video capture object
    cv2.destroyAllWindows()
    cap.release()

else:
    while True:
        # receive the image size from the master process
        img_size = comm.recv(source=0, tag=0)
        # receive the image bytes from the master process
        img_bytes = comm.recv(source=0, tag=1)

        # convert bytes to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)

        # decode numpy array to an image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # process 1 runs program 2
        if(rank == 1):
            p2(img)

        # process 2 runs program 3
        if(rank == 2):
            p3(img)

        # process 3 runs yolo function
        if(rank == 3):
            yolo_function(img)

        # check for the 'q' key pressed, to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # destroy all windows
    cv2.destroyAllWindows()
