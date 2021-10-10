"""
RentalService class
"""

from datetime import date
import unittest

import self as self

from domain.Client import Client
from domain.Movie import Movie
from repository.MovieCollection import MovieCollection
from repository.ClientBase import *
from repository.RentalHistory import RentalHistory, RentalHistoryError
from domain.Rental import Rental
from service.UndoService import FunctionCall, Operation, UndoService


class RentalServiceError(Exception):
    def __init__(self, message):
        self._message = message


class RentalService:
    """
    RentalService class is for renting and returning movies functionalities
    Attributes:
        client_repo = client repository - ClientBase
        movie_repo = movie repository - MovieCollection
        rental_repo = rental repository - RentalHistory

    Methods:
        is_client_worthy: checks if a client can rent a movie
        is_movie_available: checks if a movie is available for renting
        rent_movie: a client rents a movie
        return_movie: a client returns a movie
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

    def add_rental(self, rental):
        self.rental_repo.add_rental(rental)

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

    def is_movie_available(self, movie_id, rented_date):
        """
        Checks whether the movie is available for renting
        Args:
            movie_id: movie's id to be checked - string
            rented_date: date after which the movie is checked to be available - date

        Returns: True if available, False is not

        """
        available_date = date(1, 1, 1)
        rental_list = list(filter(lambda x: x.movie_id == movie_id, self.rental_repo.list))
        for rental in rental_list:
            if rental.returned_date is not None:
                if rental.returned_date > available_date:
                    available_date = rental.returned_date
            else:
                return False

        if available_date < rented_date:
            return True
        else:
            return False

    def rent_movie(self, movie_id, client_id, rented_date, due_date):
        """
        Adds a new rent to the rental history if it's possible
        Args:
            movie_id: the movie's id to be rented - string
            client_id: the client that rents' id - string
            rented_date: date
            due_date: date

        Returns:
        Raises: RentalServiceError in case the client is not worthy or the movie is not available

        """
        if not self.is_client_worthy(client_id):
            raise RentalServiceError("Client not worthy of any more rentals")
        elif not self.is_movie_available(movie_id, rented_date):
            raise RentalServiceError("Movie not available yet")
        else:
            rental_id = movie_id + client_id + str(rented_date) + str(due_date)
            rental = Rental(movie_id, client_id, rented_date, due_date)
            op = Operation(FunctionCall(self.rental_repo.remove_rental, rental_id),
                           FunctionCall(self.rental_repo.add_rental, rental))

            self.rental_repo.add_rental(rental)
            self.undo_service.record(op)

    def return_movie(self, movie_id, client_id, rented_date, due_date, returned_date):
        """
        Adds a returned date to a rental, marking it's end
        Args:
            movie_id: the movie's id to be rented - string
            client_id: the client that rents' id - string
            rented_date: date
            due_date: date
            returned_date: date

        Returns:
        Raises:
            ClientBaseError if client that returned not found in the client base
            RentalHistoryError if rental doesn't exist

        """

        rental_id = movie_id + client_id + str(rented_date) + str(due_date)
        rental = self.rental_repo.find_rental_by_id(rental_id)
        if rental:
            rental.returned_date = returned_date
            if returned_date > due_date:
                client = self.client_repo.find_client(client_id)
                if client:
                    client.worthy = False
                else:
                    raise ClientBaseError("Client that returned not found")

            op = Operation(FunctionCall(self.rental_repo.update_rental_returned_date, rental_id, None),
                           FunctionCall(self.rental_repo.update_rental_returned_date, rental_id, returned_date))
            self.undo_service.record(op)
        else:
            raise RentalHistoryError("Rental not found")


class TestsRentalService(unittest.TestCase):
    def setUp(self):
        
        self.rs = RentalService()
        self.rs.client_repo.add_client(Client('213', 'Mirel', True))
        self.rs.movie_repo.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        self.rs.rent_movie('566', '213', date(3, 2, 3), date(3, 3, 10))
        self.rs.return_movie('566', '213', date(3, 2, 3), date(3, 3, 10), date(3, 3, 11))

    def tearDown(self):
        self.rs.client_repo.remove_client('213')
        self.rs.movie_repo.remove_movie('566')
        self.rs.rental_repo.remove_rental('566'+'213'+str(date(3, 2, 3))+str(date(3, 3, 10)))

    def test_is_client_worthy(self):
        rs = RentalService()
        rs.client_repo.add_client(Client('212', 'Mirel', False))
        self.assertFalse(rs.is_client_worthy('212'))

    def test_is_movie_available(self):
        self.assertFalse(self.rs.is_movie_available('566', date(3, 2, 5)))
        self.assertTrue(self.rs.is_movie_available('566', date(3,4,1)))

    def test_rent_movie(self):
        rs = RentalService()
        rs.client_repo.add_client(Client('214', 'Mirel', True))
        rs.movie_repo.add_movie(Movie('567', 'Cars', 'LIFE', 'animation, adventure'))
        rs.rental_repo.add_rental(Rental('567', '214', date(2, 2, 2), date(2, 2, 11), date(2, 2, 9)))
        rs.rent_movie('567', '214', date(3,2,3), date(3,3,10))
        rid = '567' + '214' + str(date(3,2,3)) + str(date(3,3,10))
        self.assertEqual(rs.rental_repo.find_rental_by_id(rid).due_date, date(3,3,10))
        rs.undo_service.undo()
        self.assertFalse(rs.rental_repo.find_rental_by_id(rid))
        rs.undo_service.redo()
        self.assertEqual(rs.rental_repo.find_rental_by_id(rid).due_date, date(3, 3, 10))

    def test_return_movie(self):
        rid = '566' + '213' + str(date(3, 2, 3)) + str(date(3, 3, 10))
        self.assertEqual(self.rs.rental_repo.find_rental_by_id(rid).returned_date, date(3, 3, 11))
        self.rs.undo_service.undo()
        self.assertEqual(self.rs.rental_repo.find_rental_by_id(rid).returned_date, None)
        self.rs.undo_service.redo()
        self.assertEqual(self.rs.rental_repo.find_rental_by_id(rid).returned_date, date(3, 3, 11))
