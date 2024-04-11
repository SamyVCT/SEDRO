Ce projet a pour but d'implémenter des algorithmes de traitement d'images transmises en direct par un drone. Le drone utilisé pour les tests est la matrice M300RTK équipé d'une caméra H20T.
Les objectifs sont multiples :
- détecter des personnes (Yolo v8 utilisé)
- détecter une couleur spécifiée par le pilote du drone (voir extract_monochromatic_color)
- détecter les téléphones portables, talkie-walkie, montres connectées et repérer leurs positions par rapport au drone (à faire, capteur à trouver)

Une interface rassemblant les flux vidéo de chaque traitement et les données du capteur a été développée.

Pour l'instant, nous ne cherchons pas à paralléliser les calculs sur les coeurs du CPU. Le GPU GeForce RTX 3070 est assez rapide pour traiter avec Yolo en temps réel des images 1920x1080.

Utilisation de Github : 
 - pour les fichiers de plus de 100MB (weights), ajouter dans .gitignore et télécharger le fichier sur le drive


Informations : 
TOUT LE CODE ACTUELLEMENT UTILISE EST LOCALISE DANS /Interface/
Le logiciel utilise les caméras de l'ordinateur comme entrée de flux vidéo. Il est nécessaire d'utiliser le bouton update dans le menu des caméras de l'interface si vous branchez une caméra après le lancement du logiciel.
(la carte d'acquisition fonctionne comme une webcam du point de vue de l'ordinateur).
Parfois le changement de caméra peut faire freeze l'application (elle ne répond plus). Dans ce cas, il suffit d'attendre, ça finira par revenir (ça peut être assez long selon la configuration de l'ordinateur)

Le logiciel est encore dans sa version béta. Il n'est pas optimisé et des bugs peuvent être présents.


Installation (Pas fini):


Liste des bibliothèques à installer :
- ultralytics
- tk
- Pillow
- imageio
- opencv-python
- pip3 install torchvision==0.16.0+cu121 -f https://download.pytorch.org/whl/torch_stable.html3           |||| Obligatoire pour utiliser cuda (carte graphique)


Pour démarrer le programme : 
lancer le script "main.py" DEPUIS LE DOSSIER /Interface/

Attendre pour le démarrage de yolo, qui peut prendre un petit peu de temps selon la configuration.

Si l'ordinateur n'est pas équipé d'une carte graphique Nvidia : il pourrait être nécessaire de mettre en commentaire la ligne model.to('cuda') dans le fichier yolo_realtime.py




