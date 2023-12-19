import unittest
from unittest.mock import patch, MagicMock, Mock, create_autospec
from main import SSHConnection


class TestSSHConnection(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Configurer toutes les configurations ou ressources communes necessaire pour les tests
        self.ssh_connection = SSHConnection()

    @classmethod
    def tearDownClass(cls):
        # Nettoyer après que tous les tests aient été executés
        pass

    def setUp(self):
        # Configurer toutes les configurations ou ressources spécifiques aux test pour chaque test
        self.ssh_connection = SSHConnection()
        self.connection_mock = Mock()

    def tearDown(self):
        # Nettoyer après chaque cas de test
        pass

    def test_default_values(self):
        # Teste la fonction default_values
        resultat = self.ssh_connection.default_values()
        self.assertEqual(self.ssh_connection.host, '192.168.10.133')
        self.assertEqual(self.ssh_connection.user, 'user')
        self.assertEqual(self.ssh_connection.password, 'user123')
        self.assertEqual(resultat, 'Valeurs par défaut définies', msg="Résultat de la fonction default_values")

    def test_creation_and_checking_common_file(self):
        # Teste la fonction creation_and_checking_common_file()
        with patch('fabric.Connection.run') as mock_run:
            mock_run.return_value.stdout.strip.return_value = 'Bureau'
            self.ssh_connection.creation_and_checking_common_file(MagicMock())

    def test_determine_desktop(self):
        # Teste la fonction determine_desktop()
        with patch('fabric.Connection.run') as mock_run:
            mock_run.return_value.stdout.strip.return_value = '/Desktop'
            self.ssh_connection.determine_desktop(MagicMock())
            mock_run.return_value.stdout.strip.return_value = '/Bureau'
            self.ssh_connection.determine_desktop(MagicMock())

    @patch('fabric.Connection.run')
    def test_running_shell(self, run_mock):
        # Teste la fonction running_shell()
        self.ssh_connection.user = 'user'
        bureau = "Bureau"
        self.ssh_connection.shell = "test.sh"

        # Configurer le mock de la méthode run pour retourner des valeurs simulées
        # run_mock.return_value = Mock(stdout="oui", stderr="Bah nan ca a pas été run", ok=True)
        run_mock.return_value.stdout = "Résultat du shell"

        # Appel la fonction que je test
        self.ssh_connection.running_shell(self.connection_mock, "/path/to/script", "script.sh")

        self.ssh_connection.running_shell(self.connection_mock,
                                          f"/home/{self.ssh_connection.user}/{bureau}/{self.ssh_connection.shell}",
                                          self.ssh_connection.shell)

        resultat_fct = self.ssh_connection.running_shell(self.connection_mock,
                                                         f"/home/{self.ssh_connection.user}/{bureau}/dossier-commun",
                                                         self.ssh_connection.shell)

        self.assertEqual(resultat_fct, None, "Resultat de la fonction passé au test")

        resultat_run = run_mock.return_value.stdout
        self.assertEqual(resultat_run, "Résultat du shell", "Resultat de l'appel à la fonction c.run")

    @patch('fabric.Connection.get')
    @patch('main.SSHConnection.put_all_files_in')
    def test_get_files(self, mocked_get, mocked_put_all_files_in):
        # Teste la fonction get_files()
        mocked_get.return_value.stdout = "script1.txt"
        file = "script1.txt"
        not_a_file = "je /ne suis /pas un nom /de fichier $&"

        mocked_put_all_files_in.side_effect = MagicMock()

        resultat_get = self.ssh_connection.get_files(mocked_get, file)

        self.assertEqual(resultat_get, "script1.txt", msg="Appel à get_files()")

        with self.assertRaises(OSError, msg='Erreur attrapée'):
            self.ssh_connection.get_files(mocked_get, not_a_file)

        mocked_put_all_files_in.assert_not_called()

        # Ajout d'une assertion pour vérifier si la méthode put_all_files_in a été appelée ou non
        if mocked_put_all_files_in.call_count > 0:
            print("La méthode put_all_files_in a été appelée.")
        else:
            print("La méthode put_all_files_in n'a pas été appelée.")

    @patch('main.SSHConnection.clear')
    def test_menu_connection_default(self, mocked_cls):
        # Teste la fonction menu_connection() par défaut
        self.ssh_connection.default = True

        resultat = self.ssh_connection.menu_connection()

        self.assertEqual(resultat, "Valeurs par défaut définies")


if __name__ == '__main__':
    unittest.main()
