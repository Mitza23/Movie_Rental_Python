from unittest import TestCase

from domain.Client import Client
from repository.Iterable import Iterable


class ClientBaseError(Exception):
    def __init__(self, message):
        self._message = message


class ClientBase:
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

    def __init__(self, list=None):
        if list is None:
            self._list = Iterable()
        else:
            self._list = list

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, list):
        self._list = list[:]

    def find_client(self, id):
        """
        Find the client with the given id from the list
        If not found, return false
        """
        for client in self.list:
            if client.id == id:
                return client
        return False

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
        result = []
        for client in self.list:
            if client.name.lower().find(name.lower()) != -1:
                result.append(client)
        return result

    def add_client(self, client):
        """
        Adds the given Client to the list.
        Raise ClientBaseError in case that a client with the same id already found
        """
        if not self.find_client(client.id):
            self.list.append(client)
        else:
            raise ClientBaseError("Client with the same id already found")

    def remove_client(self, id):
        """
        Removes the Client with the given id from the list
        Raises ClientBaseError in case Client doesn't exist
        """
        client = self.find_client(id)
        if client:
            self.list.remove(client)
        else:
            raise ClientBaseError("Client doesn't exist in the list")

    def update_client_name(self, id, name):
        """
        Updates the name of the Client with the given id
        Raises ClientBaseError in case the Client doesn't exist
        """
        # for i in range(len(self.list)):
        #     if self.list[i].id == id:
        #         self.li
        found = False
        for customer in self.list:
            if customer.id  == id:
                customer.name = name
                found = True
        if not found:
            raise ClientBaseError("Client doesn't exist in the list")

    def update_client_id(self, id, new_id):
        """
        Updates the id of the Client with the given id
        Raises ClientBaseError in case the Client doesn't exist
        """
        # for i in range(len(self.list)):
        #     if self.list[i].id == id:
        #         self.li
        found = False
        for customer in self.list:
            if customer.id == id:
                customer.id = new_id
                found = True
        if not found:
            raise ClientBaseError("Client doesn't exist in the list")

    def update_client_worthy(self, id, worthy):
        """
        Updates the id of the Client with the given id
        Raises ClientBaseError in case the Client doesn't exist
                """
        found = False
        for customer in self.list:
            if customer.id == id:
                customer.worthy = worthy
                found = True
        if not found:
            raise ClientBaseError("Client doesn't exist in the list")



class TestClientBase(TestCase):


    def test_find_client_by_id(self):
        cb = ClientBase()
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        cl = cb.find_client('213')
        assert  cl.name == 'Mirel'


    def test_add_client(self):
        cb = ClientBase([])
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        try:
            cb.add_client(Client('687', 'Marcela'))
        except ClientBaseError as err:
            print(str(err))

    def test_remove_client(self):
        cb = ClientBase([])
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        cb.remove_client('120')
        assert not cb.find_client('120')


    def test_update_client_name(self):
        cb = ClientBase([])
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        cb.update_client_name('520', 'Gelu')
        cl = cb.find_client('520')
        assert cl.name == 'Gelu'


    def test_update_client_id(self):
        cb = ClientBase([])
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        cb.update_client_id('520', '000')
        cl = cb.find_client('000')
        assert cl.name == 'Relu'

    def test_search_client_by_id(self):
        cb = ClientBase([])
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        result = cb.search_client_by_id('2')
        self.assertEqual(len(result), 3)

    def test_search_client_by_name(self):
        cb = ClientBase([])
        cb.add_client(Client('213', 'Mirel'))
        cb.add_client(Client('520', 'Relu'))
        cb.add_client(Client('964', 'Dana'))
        cb.add_client(Client('120', 'Lorin'))
        cb.add_client(Client('687', 'Marcela'))
        result = cb.search_client_by_name('r')
        self.assertEqual(len(result), 4)


# test_find_client()
# tes_add_client()
# test_remove_client()
# test_update_client_name()
# test_update_client_id()
