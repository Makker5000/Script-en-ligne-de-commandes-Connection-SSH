# Script en ligne de commande : Connection SSH
Le Programme proposé sur ce git est un programme permettant le transfert de fichiers entre une machine hôte (votre ordinateur)
et une machine distante (une VM dans ce cas-ci pour l'exemple mais cela pourrait être un pc Linux sur le même réseau).

## Fonctionnement du programme :
### Lancer le programme :
- Soit en lançant le programme sans paramètre dans la ligne de commande le lancera par défaut.
    _Commande : python main.py_
- Soit en le lançant avec le paramètre '-m' ou '--manual_co' cela le lancera en mode connexion manuel.
    Le programme vous demandera d'entrer l'adresse ip, le username ainsi que le passaword

### Ce que propose le menu :
- Envoyer les fichiers du 'dossier-commun' vers le 'dossier-commun' de la machine distante.
    _Si vous voulez ne pas envoyer tous les fichiers il vous est recommandé de les retirer de 'dossier-commun'
    ainsi que du repertoire dans lequel votre programme est stocké._
- Récupérer les fichiers de 'dossier-commun' de la machine distante dans votre 'dossier-commun' sur votre machine hôte.
- Quitter le programme

### Choses à ne pas faire :
- Le programme accepte dans le sens _machine hôte --> machine distante_ de ré-envoyer les même fichier (ayant le même nom).
- Le programme **N'accepte PAS** de re-récupérer les fichiers de la machine distante ayant les mêmes noms (que ceux de 'dossier-commun' de votre machine hôte)
  
