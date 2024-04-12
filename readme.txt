Ce projet a pour but d'implémenter des algorithmes de traitement d'images transmises en direct par un drone. Le drone utilisé pour les tests est la matrice M300RTK équipé d'une caméra H20T.
Les objectifs sont multiples :
- détecter des personnes (Yolo v8 utilisé)
- détecter une couleur spécifiée par le pilote du drone (voir extract_monochromatic_color)
- détecter les téléphones portables, talkie-walkie, montres connectées et repérer leurs positions par rapport au drone

Une interface rassemblant les flux vidéos de chaque traitement a été développée.

Les différents traitements sont effectués en parallèle. Le GPU GeForce RTX 3070 est assez rapide pour traiter avec Yolo en temps réel des images 1920x1080.


Informations : 
TOUT LE CODE ACTUELLEMENT UTILISE EST LOCALISE DANS /SEDRO/

Le logiciel utilise les caméras de l'ordinateur comme entrée de flux vidéo. Il est nécessaire d'utiliser le bouton update dans le menu des caméras de l'interface si vous branchez une caméra après le lancement du logiciel.
(la carte d'acquisition fonctionne comme une webcam du point de vue de l'ordinateur).
Parfois le changement de caméra peut faire freeze l'application (elle ne répond plus). Dans ce cas, il suffit d'attendre, ça finira par revenir (ça peut être assez long selon la configuration de l'ordinateur)

Le choix de la détection des couleurs est assez difficile à cause de la différence de perception entre homme et machine. De ce fait, il peut être nécessaire d'effectuer quelques tests avant de lancer la recherche de personne, idéalement avec un échantillon de couleur directement vu à la caméra. 

Méthode d'utilisation détection de couleurs : Choisir la bande de couleurs à détecter en commençant par "la plus à gauche sur le spectre".
Attention : il n'est pas possible de faire un saut entre la partie la plus à gauche et la partie la plus à droite du spectre (typiquement : il n'est pas possible d'avoir l'ensemble des rouges en une seule fois).


Le logiciel est encore dans sa version béta. Il n'est pas optimisé et des bugs peuvent être présents.


Installation :


Liste des bibliothèques à installer :
- ultralytics
- tk
- Pillow
- imageio
- opencv-python
- pip3 install torchvision==0.16.0+cu121 -f https://download.pytorch.org/whl/torch_stable.html3           |||| Obligatoire pour utiliser cuda (carte graphique)


Pour démarrer le programme : 
lancer le script "main.py" DEPUIS LE DOSSIER /SEDRO/

Attendre pour le démarrage de yolo, qui peut prendre un petit peu de temps selon la configuration.

Si l'ordinateur n'est pas équipé d'une carte graphique Nvidia : il pourrait être nécessaire de mettre en commentaire la ligne model.to('cuda') dans le fichier yolo_realtime.py


///// Notes aux futurs développeurs ///// 
Les codes ont été commentés afin d'aider à la compréhension, souvent à la fois en anglais et en français. 
Important : Ne pas supprimer de classes detectées par le modèle Yolo dans le tableau de la liste des classes. Il est possible d'éventuellement les renommer. Un code a été fait pour n'afficher que les classes qui nous intéressent.

Utilisation de GitHub : 
 - pour les fichiers de plus de 100MB (weights), ajouter dans .gitignore et télécharger le fichier sur le drive.
 - Si vous souhaitez obtenir l'accès au GitHub afin de pouvoir commit, envoyez un mail à : samy.vincent@ensta-paris.fr



