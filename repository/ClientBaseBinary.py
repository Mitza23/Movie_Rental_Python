from unittest import TestCase
from domain.Client import Client
from repository.ClientBase import ClientBase, ClientBaseError
import pickle


class ClientBaseBinary(ClientBase):
    """
    The ClientBase class represents a repository for Clients
    Attributes:
        list: list of Client

    Methods:
        add_client: adds a Client to the list
        remove_client: removes a Client from the list
        update_client: changes the attributes of a Client
        find_client: finds a client in the list by the id
    """

    def __init__(self, file):
        super().__init__()
        self._file_name = file

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @staticmethod
    def string_to_obj(string):
        """
        Converts a string from the auxiliary file to a Client
        Args:
            string: string in file - string

        Returns: the client stored in the string - Client

        """
        attributes = string.strip().split(';')
        client = Client(attributes[0].strip(), attributes[1].strip(), attributes[2].strip())
        return client

    @staticmethod
    def obj_to_string(client):
        """
        Converts a Client into a string suitable for storing into the file
        Args:
            client: Client to be parsed - Client

        Returns: string denoting the client - string

        """
        string = client.id + ' ; ' + client.name + ' ; ' + str(client.worthy) + '\n'
        return string

    def load_file(self):
        """
        Loads into the repo the data found in the auxiliary file
        Returns:

        """
        try:
            f = open(self._file_name, "rb")
            string_list = pickle.load(f)
            for str in string_list:
                super(ClientBaseBinary, self).add_client(self.string_to_obj(str))
            f.close()
        except EOFError:
            raise ClientBaseError("Empty binary file")
        except IOError as e:
            raise e

    def save_file(self):
        """
        Saves into the auxiliary file the current state of the repo
        Returns:

        """
        f = open(self._file_name, "wb")
        string_list = []
        for client in self.list:
            client_str = self.obj_to_string(client)
            string_list.append(client_str)
        pickle.dump(string_list, f)
        f.close()

    def find_client(self, id):
        """
        Find the client with the given id from the list
        If not found, return false
        """
        return super(ClientBaseBinary, self).find_client(id)

    def search_client_by_id(self, id):
        """
        Finds all clients that have the given in their id
        Args:
            id: id to be searched by - string

        Returns: a list of Client

        """
        result = []
        for client in self.list:
            if client.id.find(id) != -1:
                result.append(client)
        return result

    def search_client_by_name(self, name):
        """
        Finds a list of clients with the given name in their name
        Args:
            name: name of the client - string

        Returns: list of Clients

        """
        return super(ClientBaseBinary, self).search_client_by_name(name)

    def add_client(self, client):
        """
        Adds the given Client to the list.
        Raise ClientBaseError in case that a client with the same id already found
        """
        super(ClientBaseBinary, self).add_client(client)
        self.save_file()

    def remove_client(self, id):
        """
        Removes the Client with the given id from the list
        Raises ClientBaseError in case Client doesn't exist
        """

        super(ClientBaseBinary, self).remove_client(id)
        self.save_file()

    def update_client_name(self, id, name):
        """
        Updates the name of the Client with the given id
        Raises ClientBaseError in case the Client doesn't exist
        """

        super(ClientBaseBinary, self).update_client_name(id, name)
        self.save_file()

    def update_client_id(self, id, new_id):
        """
        Updates the id of the Client with the given id
        Raises ClientBaseError in case the Client doesn't exist
        """
        super(ClientBaseBinary, self).update_client_id(id, new_id)
        self.save_file()

    def update_client_worthy(self, id, worthy):
        """
        Updates the id of the Client with the given id
        Raises ClientBaseError in case the Client doesn't exist
        """
        super(ClientBaseBinary, self).update_client_worthy(id, worthy)
        self.save_file()


# cb = ClientBaseBinary()
# cb.load_file()
# for c in cb.list:
#     print(c)
# client = cb.find_client('2')
# cb.update_client_name('2', 'Mirel')
# print(client.name, client.id)
# cb.add_client(Client('1', 'Mihai'))
# cb.add_client(Client('2', 'Vlad'))
# cb.add_client(Client('3', 'Mircea'))


class TestClientBaseBinary(TestCase):
    def setUp(self):
        self.cb = ClientBaseBinary()
        self.cb.add_client(Client('1', 'Mihai'))
        self.cb.add_client(Client('2', 'Vlad'))
        self.cb.add_client(Client('3', 'Mircea'))

    def test_add_client(self):
        self.cb.add_client(Client('4', 'Teo'))
        client = self.cb.find_client('4')
        self.assertEqual(client.name, 'Teo')

    def test_remove_client(self):
        self.cb.remove_client('2')
        self.assertFalse(self.cb.find_client('2'))

    def test_update_client_name(self):
        self.cb.update_client_name('2', 'Relu')
        self.assertEqual(self.cb.find_client('2').name, 'Relu')

    def test_update_client_id(self):
        self.cb.update_client_id('2', '10')
        self.assertEqual(self.cb.find_client('10').name, 'Vlad')

    def test_update_client_worth(self):
        self.cb.update_client_worthy('2', False)
        self.assertFalse(self.cb.find_client('2').worthy)
