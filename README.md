# Gestionnaire de tournoi d'échec

Ce script en Python permet de gérer la création, la reprise et le déroulé d'un tournoi d'échecs.


## Fonctionnalités

Le script comporte les fonctionnalités suivantes :
- Gestion d'une base de données de joueurs via un fichier .json avec :
  - nom / prénom / id d'échec / date de naissance
- Création d'un nouveau tournoi avec tracking de :
  - Date/Heure de début / fin du tournoi
  - Nom
  - Lieu
  - Nombre de tours
  - Description
- Reprise des tournois à tout moment
- Déroulé complet d'un tournoi avec archivage des résultats
- Affichage de rapport contenant :
  - Une liste des tournois sauvegardés
  - Une liste des joueurs par ordre alphabétique
  - Liste des tours et des marchs du tour

## Utilisation

Exécutez le script Python `main.py` pour lancer le programme
>python main.py

Il est possible de quitter le script à tout moment via ctrl + c, on pourra recharger l'état du programme à tout moment

Il n'est pas nécessaire de mettre en place l'environnement virtuel, le script n'utilisant pas de dépendance à installer en plus de celles par défaut.

Le rapport flake8 peut être créé via la commande
>flake8 --format=html --htmldir=flake8_rapport --exclude=env --max-line-length 119

## Auteur

Ce projet a été développé par [Guillaume Vinuesa](https://github.com/Tuxiboule).
