import unittest
from unittest.mock import patch, MagicMock
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
        # Configurer toutes les configurations ou ressources spécifiques aux test
        self.ssh_connection = SSHConnection()

    def tearDown(self):
        # Nettoyer après chaque cas de test
        pass

    def test_default_values(self):
        # Teste la fonction default_values
        self.ssh_connection.default_values()
        self.assertEqual(self.ssh_connection.host, '192.168.10.133')
        self.assertEqual(self.ssh_connection.user, 'user')
        self.assertEqual(self.ssh_connection.password, 'user123')

    def test_creation_and_checking_common_file(self):
            # Teste la fonction creation_and_checking_common_file()
            with patch('fabric.Connection.run') as mock_run:
                mock_run.return_value.stdout.strip.return_value = 'Bureau'
                self.ssh_connection.creation_and_checking_common_file(MagicMock())

    @patch('fabric.Connection')
    def test_iterative_get_files(self, mock_connection):
        # Configurer le comportement du mock
        mock_conn_instance = mock_connection.return_value
        mock_run_result = MagicMock()
        mock_run_result.stdout.split.return_value = ['file1.txt', 'file2.txt']
        mock_conn_instance.run.return_value = mock_run_result

        # Instancier votre classe (ou la classe contenant la fonction iterative_get_files)
        your_instance = SSHConnection()

        # Appeler la fonction testée
        your_instance.iterative_get_files(mock_conn_instance, '/home/user/Bureau/dossier-commun/')

        # Vérifier l'utilisation correcte du mock
        mock_connection.assert_called_once_with(host='192.168.10.133', user='user',
                                                connect_kwargs={'password': 'user123'})
        mock_conn_instance.run.assert_called_once_with('ls /home/user/Bureau/dossier-commun/', hide=True)
        mock_conn_instance.get.assert_called_with('/home/user/Bureau/dossier-commun/file1.txt', local=None,
                                                  preserve_mode=True)

    # Ajouter d'autres tests au besoin
    # ...


if __name__ == '__main__':
    unittest.main()
