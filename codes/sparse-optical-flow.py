import cv2 as cv
import numpy as np
import statistics
import collections


########################## Définition des paramètres et initialisation : ##########################

# Chemin de la vidéo sur laquelle on travaille
FILE = "video.MP4"

# Paramètres pour la détection de coins par l'algorithme de Shi-Tomasi
feature_params = dict(maxCorners = 300, qualityLevel = 0.5, minDistance = 2, blockSize = 7)
# Paramètres pour l'algorithme de Lucas-Kanade (flot optique)
lk_params = dict(winSize = (7,7), maxLevel = 2,
    criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
# Couleur des points de tracking sur la vidéo de retour
color = (0, 255, 0)

# Import de la vidéo dans un objet OpenCV de type VideoCapture
cap = cv.VideoCapture(FILE)

# Lecture de la 1ère image
# ret = booléen attestant la réussite de la lecture
# first_frame = 1ère image de la vidéo
ret, first_frame = cap.read()

# Paramètre de sortie
OUTPUT = False

# Préparation de l'export de la vidéo de sortie
if (OUTPUT) :
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter("./outputs/output.mp4",fourcc, float(24), (int(cap.get(3)),int(cap.get(4))))


############################ Détections des coins dans la 1ère image : ############################

# Conversion de l'image en nuance de gris car seule la luminance est nécessaire pour la détection de
# coins et le calcul est alors moin coûteux.
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
# Recherche des coins par la méthode Shi-Tomasi -> seront les points sur lesquels nous allons
# appliquer le flot optique
# https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack
prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
# Création de l'image qui contiendra la trace de tous les points traqués. Initialiation nulle.
mask = np.zeros_like(first_frame)


############################ Boucle sur toute les images de la vidéo : ############################

# Tant que la vidéo n'est pas terminée
while(cap.isOpened()):

    # Lecture de l'image suivante
    ret, frame = cap.read()
    # Conversion de cette image en nuance de gris
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    ################################ Calcul du flot optique : #################################

    # Calcul du flot optique par la méthode de Lucas-Kanade sur les points détecté précédements
    # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
    next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)
    # en sortie de cette fonction :
    # next : prédiction des nouvelles coordonées des points dans l'image suivante
    # status : tableau de booléen indiquant si les nouvelles positions ont pu être calculée
    # error : vecteur de l'erreur sur les positions

    # Sélection des points dont les positions ont pu être calculée
    good_old = prev[status == 1].astype(int)
    good_new = next[status == 1].astype(int)


    ############################# Traitement des points obtenus : #############################

    # Calcul de la variation des coordonées des points et de leur vitesse
    variation = good_new-good_old
    speed = [((variation[i][0]),(variation[i][1])) for i in range(len(variation))]
    # Répartition des vitesses
    repartition = collections.Counter(speed)
    repartition_key = [item[0] for item in repartition.items()]
    repartition_value = [item[1] for item in repartition.items()]
    # Sélection des indices des points dont la répartition des vitesses est la plus élevée
    rejected_points = [repartition_key[i] for i in range(len(repartition_key)) if (len(repartition_key)>1 and repartition_value[i]>statistics.quantiles(repartition_value, n=4)[0])]
    # Liste des coordonées de ces points
    interesting_points_old, interesting_points_new = [], []
    i=0
    for value in speed :
        if not (value in rejected_points) :
            interesting_points_old.append(good_old[i])
            interesting_points_new.append(good_new[i])
        i += 1


    ########################### Dessin des traces du flot optique : ###########################

    for i, (new, old) in enumerate(zip(interesting_points_old, interesting_points_new)):
        # Renvoie les coordonées des nouveaux points
        a, b = new.ravel()
        # Renvoie les coordonées des anciens points
        c, d = old.ravel()
        # Trace une ligne entre les vieux et les nouveaux points
        mask = cv.line(mask, (a, b), (c, d), color, 2)
        # Affiche un cercle sur la position des nouveaux points
        frame = cv.circle(frame, (a, b), 3, color, -1)
    # Affiche le flot optique par dessus la vidéo
    output = cv.add(frame, mask)
    # Mise à jour de la nouvelle frame
    prev_gray = gray.copy()

    # Ouverture d'une fenêtre pour afficher la sortie
    cv.imshow("sparse optical flow", output)



    # Mise à jour des points d'intérêt
    prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)

    # Arrêt du programme si l'utilisateur presse la touche 'q'
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

    # Enregistrement de la vidéo si précisé
    if (OUTPUT) :
        out.write(output)

# Libération des ressources et fermeture des fenêtre
cap.release()
if (OUTPUT) :
    out.release()
cv.destroyAllWindows()
