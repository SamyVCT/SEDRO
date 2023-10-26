Programmes développés l'année dernière :

    programme1.py
    programme2.py
    programme3.py
    sparse-optical-flow.py


Réécriture de ces programmes en fichiers de fonctions pour une possible parallélisation de la tâche d'identification d'image et utilisation des codes développés :

    p2_function.py (fonction du programme 2)
    p3_function.py (fonction du programme 3)

Code que implemente YOLO:
    yolos/yolo.py

parallel_identifier.py (programme qui parallélise l'identification, en envoyant l'entrée vidéo aux autres programmes - il doit être amélioré, mais fonctionne déjà)


Pour les faire marcher:
Il faut installer:

- mpi4py
- OpenMPI

En plus pour utiliser le YOLO il faut installer les weigths de le reseau (l'archive est disponible partout) et le mettre dans le fichier yolos:

- yolov3.weights

Après pour executer:
mpiexec -n 3 python3 parallel_identifier.py 

(Vous pouvez changer le nombre de coeurs utilisé, regardez le logiciel parallel_identifier pour savoir comment ils sont reparties)
(Dans le logiciel parallel_identifier.py vous pouvez changer l'ordre des fonctions)

fichier yolo (implémentation récente d'un identificateur plus précis, utilisant la bibliothèque YOLO - You Only Look Once)