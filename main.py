from fabric import Connection,Config
from getpass import getpass
import os
import argparse
import time


class SSHConnection:
    def __init__(self):
        self.host = ''
        self.user = ''
        self.password = ''

        self.choice = ["1", "2", "3"]
        self.the_choice = ""
        self.vrai = True
        self.default = False
        self.path = "/home/user/Bureau/"
        self.path_for_shell = "/home/user/Bureau/"
        self.shell = "test.sh"
        self.remote_path_common_files = "/home/user/Bureau/dossier-commun/"
        self.path_to_local_file = ""

    def default_values(self):
        """
        Fonction ayant les informations de connexion par défaut. Si pas de paramètre passé lors de
        l'éxécution du programme
        :PRE: -
        :POST: -
        """
        self.host = '192.168.10.133'
        self.user = 'user'
        self.password = 'user123'

    @staticmethod
    def clear() -> None:
        """
        Fonction qui efface l'écran de la console
        :PRE: -
        :POST: -
        """
        os.system('cls')

    def menu_connection(self):
        """
        Fonction qui va afficher le menu de connection si jamais l'utilisateur a lancé le programme
        avec le paramètre adéquat pour se connecter manuellement
        :PRE: -
        :POST: -
        """
        self.clear()
        if self.default:
            print("Vous avez décidé de vous connecter à la machine par défaut...")
            time.sleep(2)
            self.default_values()
        else:
            print("Vous avez décidé de vous connecter en manuel")
            self.host = input("> L'adresse IP de l'appareil auquel vous voulez vous ¨connecter : ")
            self.user = input("> Votre Username : ")
            self.password = getpass("> Et votre mot de passe : ")

    @staticmethod
    def determine_desktop(c):
        """
        Fonction qui va déterminer si le système d'exploitation de la
        machine distante est en Anglais ou en Françcais.
        :PRE: -
        :POST: -
        """
        # Utiliser la commande shell pour déterminer si le bureau est en français ou en anglais sur le PC distant
        result_temp = c.run("test -d ~/Bureau && echo Bureau || (test -d ~/Desktop && echo Desktop || echo Unknown)",
                            hide=True)
        bureau_desktop_temp = result_temp.stdout.strip()
        return f"/{bureau_desktop_temp}"

    def creation_and_checking_common_file(self, c):
        """
        Fonction qui vérifie si le dossier 'dossier-commun' existe sur la machine hôte et sur la machine distante.
        Si jamais il n'existe pas sur une des deux machines ou bien les deux alors il créer le dossier.
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
        :POST: -
        """
        # Déterminer si le bureau est en français ou en anglais
        """if os.path.exists(os.path.join(os.path.expanduser('~'), 'Bureau')):
            bureau_desktop = '/Bureau'
        elif os.path.exists(os.path.join(os.path.expanduser('~'), 'Desktop')):
            bureau_desktop = '/Desktop'
        else:
            print("Impossible de déterminer le chemin du bureau.")
            return"""

        name_of_file = "dossier-commun"
        self.path_to_local_file = os.path.join(os.getcwd(), name_of_file)
        # Vérifier sur l'hôte local
        if not os.path.exists(self.path_to_local_file):
            os.makedirs(self.path_to_local_file)
            print(f"Le dossier '{self.path_to_local_file}' a été créé sur l'hôte local.")

        bureau_desktop = self.determine_desktop(c)
        self.path = "/home/" + self.user + bureau_desktop
        # Vérifier sur le PC distant
        result = c.run(f"test -d {self.path}/{name_of_file} && echo 1 || echo 0", hide=True)
        if result.stdout.strip() == '0':
            # Le dossier n'existe pas sur le PC distant, créons-le
            c.run(f"mkdir -p {self.path}/{name_of_file}")
            print(f"Le dossier '{name_of_file}' a été créé sur le PC distant dans '{self.path}'.")

        self.path += "/" + name_of_file
        time.sleep(2.5)

    def menu_main(self, c):
        """
        Fonction qui va être appelée afin de proposer le menu principal et qui permet
        à l'utilisateur de faire un choix.
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
        :POST: -
        """
        self.creation_and_checking_common_file(c)
        self.clear()
        if self.default:
            self.running_shell(c, self.path_for_shell, self.shell)

        if self.default:
            print(f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                  f"\n+ Vous pouvez également vous connecter à une machine manuellement                               +\n"
                  "+ Il vous faut introduire le paramètre '-m' ou bien '--manual_co' derrière le nom du programme  +\n"
                  "+ lorsque vous le lancez via la concole                                                         +\n"
                  "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        print(f"Vous voici dans le Menu Principal, vous êtes connecté en SSH.\n\n"
              f"Que voulez vous faire parmi : \n"
              f"{self.choice[0]}. Récuperer les fichiers sur la machine distante\n"
              f"{self.choice[1]}. Envoyer des fichiers sur la machine distante\n"
              f"{self.choice[2]}. Quitter le programme\n")

        self.the_choice = input("> Ton choix ? ")
        print(self.the_choice)

    def running_shell(self, c, pth, sh):
        """
        Fonction qui va executer un fichier shell se trouvant sur la machine distante et qui va
        récupérer des données systèmes
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
              - pth : Le chemin où se trouve le script shelle sur la machine distante par défaut
              - sh : Le nom du fichier shell à éxécuter
        :POST: -
        """
        print(f"En cours de récupération des données système de la machine distante...")
        result = c.run(f"cd {pth} && ./{sh}", hide="stdout")
        self.clear()
        print(result.stdout)
        self.vrai = False

    @staticmethod
    def put_all_files_in():
        """
        Fonction qui met tous les fichiers du répertoire courant (sauf 'main.py', '.idea', '.git' et 'dossier-commun')
        dans 'dossier-commun' sur machine hôte
        :PRE: -
        :POST: -
        """
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

    @staticmethod
    def get_all_files_in():
        """
        Fonction qui récupère tous les fichiers de 'dossier-commun'
        et les mets dans le répertoire courant de la machine hôte
        :PRE: -
        :POST: -
        """
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
        """
        Fonction qui va aller chercher le fichier spécifier sur la machine distante.
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
              - remote_file : Le nom du fichier à récupérer
        :POST: -
        """
        try:
            c.get(f"/home/user/Bureau/dossier-commun/{remote_file}", local=None, preserve_mode=True)
            self.put_all_files_in()
        except OSError as o:
            print(f"Erreur lors du téléchargement : {o}")

    def send_files(self, c, local_files):
        """
        Fonction qui envoi les fichiers du répertoire courant de la machine hôte
        (sauf 'main.py', '.idea', '.git' et 'dossier-commun') dans 'dossier-commun' de la machine distante.
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
              - local_files : Le nom du fichier à envoyer
        :POST: -
        """
        try:
            c.put(local_files, self.remote_path_common_files)
        except OSError as o:
            print(f"Erreur lors du téléchargement : {o}")

    def iterative_send_files(self, c):
        """
        Fonction qui va parcourir le répertoire courant de la machine hôte et appeler itérativement
        la fonction send_files() qui va à son tour ajouter les fichiers à 'dossier-commun'.
        de la machine distante
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
        :POST: -
        """
        self.get_all_files_in()

        # Définir le répertoire courant
        current_rep = os.getcwd()

        # Liste des fichiers et dossiers à exclure
        exclusions = {'main.py', '.idea', '.git', 'dossier-commun'}

        # Parcourir tous les fichiers du répertoire courant
        for file in os.listdir(current_rep):
            # Vérifier si le fichier ne fait pas partie des exclusions
            if file not in exclusions:
                # Déplacer le fichier vers le dossier 'dossier-commun'
                self.send_files(c, file)
                print(f"Le fichier {file} a été ajouté dans la VM")

        self.put_all_files_in()

    def iterative_get_files(self, c, remote_path):
        """
        Fonction qui va parcourir le répertoire courant de la machine distante et appeler itérativement
        la fonction get_files() qui va à son tour recupérer les fichiers de 'dossier-commun'
        de la machine distante pour les mettre dans 'dossier-commun' de la machine hôte tout en vérifiant si ils
        n'existent pas déjà.
        :PRE: - c : L'instance de connection SSH de l'objet 'Connection' provenant de la librairie 'Fabric'
              - remote_path : Le chemin du répertoire des fichiers à récupérer sur la machine distante
        :POST: -
        """
        result = c.run(f"ls {remote_path}", hide=True)

        list_files = result.stdout.split()

        for file in list_files:
            current_rep = os.path.join(os.getcwd(), 'dossier-commun', file)
            if not os.path.exists(current_rep):
                self.get_files(c, file)
            else:
                return "Erreur"

        self.put_all_files_in()

    def is_continuing(self):
        yes = ['oui', 'o']
        no = ['no', 'n']
        finis = False
        print("\nVoulez-vous faire d'autres opérations ? (o/n)")
        while not finis:
            choice = input(">> ")
            if choice.lower() == yes[0] or choice.lower() == yes[1]:
                self.vrai = True
                finis = True
            elif choice.lower() == no[0] or choice.lower() == no[1]:
                self.vrai = False
                print("Au revoir !")
                finis = True
            else:
                finis = False

    def run(self):
        """
        Fonction principale du programme qui est appelée en première et qui appelle à son tour les autres fonctions.
        :PRE: -
        :POST: -
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--manual_co", help="Sert à lancer le programme en mode connection manuel", action="store_true")
        args = parser.parse_args()

        if args.manual_co:
            self.default = False
        else:
            self.default = True
        self.menu_connection()
        try:
            # Créer une connexion SSH en utilisant le mot de passe
            with Connection(host=self.host, user=self.user, connect_kwargs={'password': self.password}) as conn:
                while self.vrai:
                    self.menu_main(conn)
                    if self.the_choice == self.choice[0]:
                        print("Vous avez decidé de récupérer les fichiers provenant de la machine distante.\n")
                        self.iterative_get_files(conn, self.remote_path_common_files)
                        print("\nAllez voir votre répertoire 'dossier-commun' sur votre machine hôte.")
                        #self.vrai = False
                        self.is_continuing()
                    elif self.the_choice == self.choice[1]:
                        print("Vous avez décidé d'envoyer des fichiers sur la machine distante.\n")
                        self.iterative_send_files(conn)
                        print("\nAllez voir le répertoire 'dossier-commun' sur la machine distante (si vous le pouvez).")
                        #self.vrai = False
                        self.is_continuing()
                    elif self.the_choice == self.choice[2]:
                        print("Vous avez décidé de quitter, au revoir !")
                        self.vrai = False
                    else:
                        print("Entrez un nombre valide !")
                        self.vrai = True

        except TimeoutError:
            print("Temps dépassé, réessayez svp")
            input("Appuyez sur une touche pour continuer et ressayer...")
            self.run()


if __name__ == "__main__":
    ssh_co = SSHConnection()
    ssh_co.run()
