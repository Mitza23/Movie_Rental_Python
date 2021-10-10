import unittest
from datetime import date

from domain.Client import Client
from domain.Movie import Movie
from domain.Rental import Rental
from repository.ClientBase import ClientBase, ClientBaseError
from repository.MovieCollection import MovieCollection
from repository.RentalHistory import RentalHistory
from service.UndoService import FunctionCall, Operation, UndoService, CascadedOperation


class ClientServiceError(Exception):
    """
    ClientServiceError handles errors occurred in operations regarding clients
    """
    def __init__(self, message):
        self._message = message


class ClientService:
    """
    ClientService class is for removing clients
    Attributes:
        client_repo = client repository - ClientBase
        movie_repo = movie repository - MovieCollection
        rental_repo = rental repository - RentalHistory

    Methods:
        remove_client: removes client from the repo and all the rental associated to it
    """
    def __init__(self, client_base=None, movie_collection=None, rental_history=None, undo_service=None):
        if client_base is None:
            client_base = ClientBase()
        if movie_collection is None:
            movie_collection = MovieCollection()
        if rental_history is None:
            rental_history = RentalHistory()
        if undo_service is None:
            undo_service = UndoService()
        self._client_repo = client_base
        self._movie_repo = movie_collection
        self._rental_repo = rental_history
        self._undo_service = undo_service

    @property
    def client_repo(self):
        return self._client_repo

    @property
    def movie_repo(self):
        return self._movie_repo

    @property
    def rental_repo(self):
        return self._rental_repo

    @property
    def undo_service(self):
        return self._undo_service

    def is_client_worthy(self, client_id):
        """
        Checks whether a client is worthy of rentals
        Args:
            client_id: id of the client to be checked - string

        Returns: True is it is False if not
        Raises ClientBaseError if client not found

        """
        client = self.client_repo.find_client(client_id)
        if not client:
            raise ClientBaseError("Client not found")
        elif not client.worthy:
            return False
        return True

    def remove_client(self, client_id):
        """
        Removes the client with the given id from the client repo and all the rentals associated with it
        Args:
            client_id: id of client - string

        Returns:

        """
        casop = CascadedOperation()

        rental_list = list(filter(lambda x: x.client_id == client_id, self.rental_repo.list))
        ok = True
        for rt in rental_list:
            if rt.returned_date is None:
                ok = False
        if not ok:
            raise ClientServiceError("Client can't be removed as it has a rental in process")
        else:
            for rental in rental_list:
                op = Operation(FunctionCall(self.rental_repo.add_rental, rental),
                               FunctionCall(self.rental_repo.remove_rental, rental.id))
                casop.add_operation(op)
                self.rental_repo.remove_rental(rental.id)

            client = self.client_repo.find_client(client_id)
            op = Operation(FunctionCall(self.client_repo.add_client, client),
                           FunctionCall(self.client_repo.remove_client, client_id))
            casop.add_operation(op)
            self.client_repo.remove_client(client_id)
            self.undo_service.record(casop)

    def add_client(self, client):
        """
        Adds a client to the repo
        Args:
            client: client ot be added - Client

        Returns:

        """
        self.client_repo.add_client(client)
        undo = FunctionCall(self.client_repo.remove_client, client.id)
        redo = FunctionCall(self.client_repo.add_client, client)
        op = Operation(undo, redo)
        self.undo_service.record(op)

    def update_client_name(self, client_id, client_name):
        """
        Updates the name of the client with the given id
        Args:
            client_id: id of the client - string
            client_name: updated name - string

        Returns:

        """
        initial_name = self.client_repo.find_client(client_id).name
        op = Operation(FunctionCall(self.client_repo.update_client_name, client_id, initial_name),
                       FunctionCall(self.client_repo.update_client_name, client_id, client_name))
        self.client_repo.update_client_name(client_id, client_name)
        self.undo_service.record(op)

    def update_client_worthy(self, client_id, worth):
        """
        Updates the worth of the client with the given id
        Args:
            client_id: id of the client - string
            worth: updated worth - bool

        Returns:

        """
        initial_worth = self.client_repo.find_client(client_id).worthy
        op = Operation(FunctionCall(self.client_repo.update_client_worthy, client_id, initial_worth),
                       FunctionCall(self.client_repo.update_client_worthy, client_id, worth))
        self.client_repo.update_client_worthy(client_id, worth)
        self.undo_service.record(op)


class TestClientService(unittest.TestCase):
    def setUp(self):
        self.cs = ClientService()
        self.cs.movie_repo.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        self.cs.client_repo.add_client(Client('213', 'Mirel', True))
        self.cs.rental_repo.add_rental(Rental('566', '213', date(2,2,2), date(2,2,10), date(2,2,9)))

    def test_is_client_worthy(self):
        self.assertEqual(self.cs.is_client_worthy('213'), True)
        with self.assertRaises(ClientBaseError):
            self.cs.is_client_worthy('1')

    def test_remove_client(self):
        self.cs.remove_client('213')
        self.assertEqual(len(self.cs.rental_repo.list), 0)
        self.assertEqual(len(self.cs.client_repo.list), 0)
        self.cs.undo_service.undo()
        self.assertEqual(self.cs.client_repo.find_client('213').name, 'Mirel')
        self.cs.undo_service.redo()
        self.assertEqual(len(self.cs.rental_repo.list), 0)
        self.assertEqual(len(self.cs.client_repo.list), 0)

    def test_add_client(self):
        self.cs.add_client(Client('1', 'a'))
        self.assertEqual(len(self.cs.client_repo.list), 2)
        self.cs.undo_service.undo()
        self.assertFalse(self.cs.client_repo.find_client('1'))
        self.cs.undo_service.redo()
        self.assertEqual(self.cs.client_repo.find_client('1').name, 'a')

    def test_update_client_name(self):
        self.cs.update_client_name('213', 'Mirelian Rex')
        self.assertEqual(self.cs.client_repo.find_client('213').name,  'Mirelian Rex')
        self.cs.undo_service.undo()
        self.assertEqual(self.cs.client_repo.find_client('213').name, 'Mirel')
        self.cs.undo_service.redo()
        self.assertEqual(self.cs.client_repo.find_client('213').name, 'Mirelian Rex')

    def test_update_client_worthy(self):
        self.cs.update_client_worthy('213', False)
        self.assertEqual(self.cs.client_repo.find_client('213').worthy, False)
        self.cs.undo_service.undo()
        self.assertEqual(self.cs.client_repo.find_client('213').worthy, True)
        self.cs.undo_service.redo()
        self.assertEqual(self.cs.client_repo.find_client('213').worthy, False)

