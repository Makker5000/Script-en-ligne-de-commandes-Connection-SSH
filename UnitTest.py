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

    @patch('fabric.Connection.run')
    def test_creation_and_checking_common_file(self, mock_run):
        # Teste la fonction determine_desktop à partir du moment où elle est appelée dans creation_and_checking_common_file
        with patch.object(self.ssh_connection, 'determine_desktop', return_value='/Bureau'):
            # Calling the creation_and_checking_common_file method
            self.ssh_connection.creation_and_checking_common_file(MagicMock())

        mock_run.assert_called_with("test -d /home/user/Bureau/dossier-commun && echo 1 || echo 0", hide=True)

    def test_creation_and_checking_common_file(self):
            # Teste la fonction creation_and_checking_common_file()
            with patch('fabric.Connection.run') as mock_run:
                mock_run.return_value.stdout.strip.return_value = 'Bureau'
                self.ssh_connection.creation_and_checking_common_file(MagicMock())


if __name__ == '__main__':
    unittest.main()
