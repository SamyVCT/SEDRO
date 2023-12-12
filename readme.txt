Ce projet a pour but d'implémenter des algorithmes de traitement d'images transmises en direct par un drone. Le drone utilisé pour les tests est la matrice M300RTK équipé d'une caméra H20T.
Les objectifs sont multiples :
- détecter des personnes (Yolo v8 utilisé)
- détecter une couleur spécifiée par le pilote du drone (voir extract_monochromatic_color)
- détecter les téléphones portables, talkie-walkie, montres connectées et repérer leurs positions par rapport au drone (à faire, capteur à trouver)

Une interface rassemblant les flux vidéo de chaque traitement et les données du capteur a été développée.

Pour l'instant, nous ne cherchons pas à paralléliser les calculs sur les coeurs du CPU. La GPU GeForce RTX 3070 est assez rapide pour traiter avec Yolo en temps réelle des images 1920x1080.

Utilisation de Github : 
 - pour les fichiers de plus de 100MB (weights), ajouter dans .gitignore et télécharger le fichier sur le drive

