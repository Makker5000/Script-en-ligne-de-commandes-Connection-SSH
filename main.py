from fabric import Connection,Config
from getpass import getpass
import os
import argparse

class SSH_connection:
    def __init__(self):
        # Remplacez ces valeurs par les informations de connexion appropriées
        """
        self.host = '192.168.10.133'
        self.user = 'user'
        self.password = 'user123'
        """
        self.host = ''
        self.user = ''
        self.password = ''

        self.choice = ["1", "2", "3"]
        self.the_choice = ""
        self.vrai = True
        self.default = False
        self.path = "/home/user/Bureau/"
        self.shell = "test.sh"
        # pour le 'put()'
        #self.local_files = os.path.join('file_from_Windows.txt')
        self.remote_path_common_files = "/home/user/Bureau/dossier-commun/"

        # pour le 'get()'
        #self.remote_file = "/home/user/Bureau/dossier-commun/file_from_Linux.txt"
        self.remote_path = "/home/user/Bureau/dossier-commun/"
        #self.local_path_common_files = r"C:\Users\pc\OneDrive - EPHEC asbl\Bureau\Cours\Cours 2ème\Dev 2\TLCA-Interro-devoirs\Script-en-ligne-de-commande\Script-en-ligne-de-commandes-Connection-SSH\dossier-commun"
        #self.local_path_common_files = os.path.join(os.getcwd(), 'dossier-commun')



    def __str__(self):
        pass

    def default_values(self):
        self.host = '192.168.10.133'
        self.user = 'user'
        self.password = 'user123'

    def clear(self):
        os.system('cls')

    def menu_connection(self):
        self.clear()
        #print(f"Bienvenu dans le programme se connectant en SSH\n")
        if self.default:
            print("Vous avez décidé de vous connecter a la machine par défaut...")
            self.default_values()
        else:
            print("Vous avez décidé de vous connecter en manuel")
            self.host = input("> L'adresse IP de l'appareil auquel vous voulez vous ¨connecter : ")
            self.user = input("> Votre Username : ")
            self.password = getpass("> Et votre mot de passe : ")

    def menu_main(self, c):
        self.clear()
        # self.running_shell(c, self.path, self.shell)
        print(f"Vous voici dans le Menu Principal, vous êtes connecté en SSH.\n"
              f"Que voulez vous faire parmi : \n"
              f"{self.choice[0]}. Récuperer les fichiers sur la machine distante\n"
              f"{self.choice[1]}. Envoyer des fichiers sur la machine distante\n"
              f"{self.choice[2]}. Quitter le programme\n")

        self.the_choice = input("> Ton choix ? ")
        print(self.the_choice)

    def running_shell(self, c, pth, sh):
        print(f"En cours de récupération des données système de la machine distante...")
        result = c.run(f"cd {pth} && ./{sh}", hide="stdout")
        self.clear()
        print(result.stdout)
        self.vrai = False


    # Après utilisationde la fonction get()
    def put_all_files_in(self):
        # Définir le répertoire courant
        current_rep = os.getcwd()

        # Créer le dossier 'dossier-commun' s'il n'existe pas encore
        dossier_commun = os.path.join(current_rep, 'dossier-commun')
        if not os.path.exists(dossier_commun):
            os.makedirs(dossier_commun)
            print(f"Le dossier '{dossier_commun}' a été créé.")

        # Liste des fichiers et dossiers à exclure
        exclusions = {'main.py', '.idea', '.git', 'dossier-commun'}

        # Parcourir tous les fichiers du répertoire courant
        for file in os.listdir(current_rep):
            file_path = os.path.join(current_rep, file)

            # Vérifier si le fichier ne fait pas partie des exclusions
            if file not in exclusions:
                # Déplacer le fichier vers le dossier 'dossier-commun'
                destination = os.path.join(dossier_commun, file)
                os.rename(file_path, destination)
                print(f"Le fichier '{file}' a été déplacé vers '{dossier_commun}'.")

    # Lorsque la fonction put() est appelée
    def get_all_files_in(self):
        # Définir le répertoire courant
        current_rep = os.getcwd()

        # Dossier 'dossier-commun'
        dossier_commun = os.path.join(current_rep, 'dossier-commun')

        # Vérifier si le dossier 'dossier-commun' existe
        if os.path.exists(dossier_commun) and os.path.isdir(dossier_commun):
            # Parcourir tous les fichiers du dossier 'dossier-commun'
            for file in os.listdir(dossier_commun):
                file_path = os.path.join(dossier_commun, file)

                # Déplacer le fichier vers le répertoire courant
                destination = os.path.join(current_rep, file)
                os.rename(file_path, destination)
                print(f"Le fichier '{file}' a été déplacé vers '{current_rep}'.")
        else:
            print(f"Le dossier '{dossier_commun}' n'existe pas.")

    def get_files(self, c, remote_file):
        try:
            c.get(f"/home/user/Bureau/dossier-commun/{remote_file}", local=None, preserve_mode=True)
            print("Allez voir votre dossier")
            self.put_all_files_in()
        except OSError as o:
            print(f"Erreur lors du téléchargement : {o}")


    def send_files(self, c, local_files):
        try:
            c.put(local_files, self.remote_path_common_files)
        except OSError as o:
            print(f"Erreur lors du téléchargement : {o}")


    def iterative_send_files(self, c):
        self.get_all_files_in()

        # Définir le répertoire courant
        current_rep = os.getcwd()

        # Liste des fichiers et dossiers à exclure
        exclusions = {'main.py', '.idea', '.git', 'dossier-commun'}

        # Parcourir tous les fichiers du répertoire courant
        for file in os.listdir(current_rep):
            chemin_fichier = os.path.join(current_rep, file)
            # Vérifier si le fichier ne fait pas partie des exclusions
            if file not in exclusions:
                # Déplacer le fichier vers le dossier 'dossier-commun'
                self.send_files(c, file)
                print(f"Le fichier {file} a été ajouté dans la VM")

        self.put_all_files_in()

    def iterative_get_files(self, c, remote_path):
        result = c.run(f"ls {remote_path}", hide=True)

        list_files = result.stdout.split()

        for file in list_files:
            self.get_files(c, file)

        self.put_all_files_in()


    def run(self):
        """with Connection(host='192.168.10.133', user='user') as conn:
            result = conn.run('echo Hello, Fabric!')
            print(result.stdout)
            result = conn.run("ls -la", hide=True)
            print(result.stdout)"""

        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--manual_co", help="Sert à lancer le programme en mode connection manuel", action="store_true")
        args = parser.parse_args()

        if args.manual_co:
            self.default = False
        else:
            self.default = True
        self.menu_connection()
        try:
            # Créez une connexion SSH en utilisant le mot de passe
            with Connection(host=self.host, user=self.user, connect_kwargs={'password': self.password}) as conn:
                # Exécutez la commande 'ls -a' à distance
                # result = conn.run('ls -a', hide=True)
                # Affichez le résultat
                # print(f'Résultat de la commande "ls -a" sur {self.host}:\n{result.stdout}')

                while self.vrai:
                    self.menu_main(conn)
                    if self.the_choice == self.choice[0]:
                        print("Tu veux Récup des fichiers ? ")
                        self.iterative_get_files(conn, self.remote_path)
                        self.vrai = False
                    elif self.the_choice == self.choice[1]:
                        print("AAAAAh tu veux envoyer des fichiers sur l'autre")
                        self.iterative_send_files(conn)
                        self.vrai = False
                    elif self.the_choice == self.choice[2]:
                        self.vrai = False
                    else:
                        print("Entre un nombre valide !")
                        self.vrai = False

        except TimeoutError:
            print("Temps dépassé, réessayez svp")
            input("Appuie sur une touche pour continuer...")
            self.run()

if __name__ == "__main__":
    ssh_co = SSH_connection()
    ssh_co.run()
