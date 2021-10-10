"""
MovieService class
"""
import unittest
from datetime import date

from domain.Client import Client
from domain.Movie import Movie
from domain.Rental import Rental
from repository.ClientBase import ClientBase
from repository.MovieCollection import MovieCollection
from repository.RentalHistory import RentalHistory
from service.UndoService import FunctionCall, Operation, UndoService, CascadedOperation


class MovieServiceError(Exception):
    """
    MovieServiceError handles errors related to MovieService class
    """
    def __init__(self, message):
        self._message = message


class MovieService:
    """
    MovieService class used for removing movies
    Attributes:
        client_repo = client repository - ClientBase
        movie_repo = movie repository - MovieCollection
        rental_repo = rental repository - RentalHistory
    Methods:
        remove_movie: removes a movie from the repo and all rental associated to it
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

    def remove_movie(self, movie_id):
        """
        Removes a movie and all rentals related to it
        Args:
            movie_id: id of movie - string

        Returns:

        """
        casop = CascadedOperation()
        rental_list = list(filter(lambda x: x.movie_id == movie_id, self.rental_repo.list))
        ok = True
        for rt in rental_list:
            if rt.returned_date is None:
                ok = False
        if not ok:
            raise MovieServiceError("Movie can't be removed as it has a rental in process")
        else:
            for rental in rental_list:
                self.rental_repo.remove_rental(rental.id)
                op = Operation(FunctionCall(self.rental_repo.add_rental, rental),
                               FunctionCall(self.rental_repo.remove_rental, rental.id))
                casop.add_operation(op)

            movie = self.movie_repo.find_movie(movie_id)
            op = Operation(FunctionCall(self.movie_repo.add_movie, movie),
                           FunctionCall(self.movie_repo.remove_movie, movie_id))
            casop.add_operation(op)
            self.movie_repo.remove_movie(movie_id)
            self.undo_service.record(casop)

    def add_movie(self, movie):
        """
        Adds a new movie to the repo
        :param movie: movie to be added - Movie
        :return:
        """
        self.movie_repo.add_movie(movie)
        undo = FunctionCall(self.movie_repo.remove_movie, movie.id)
        redo = FunctionCall(self.movie_repo.add_movie, movie)

        op = Operation(undo, redo)
        self.undo_service.record(op)

    def update_movie_title(self, movie_id, value):
        """
        Updating a movie's title by id
        :param movie_id: movie's id of which title is updated - string
        :param value: value to which the title is updated - string
        :return:
        """
        initial_value = self.movie_repo.find_movie(movie_id).title
        op = Operation(FunctionCall(self.movie_repo.update_movie_title, movie_id, initial_value),
                       FunctionCall(self.movie_repo.update_movie_title, movie_id, value))
        self.undo_service.record(op)
        self.movie_repo.update_movie_title(movie_id, value)

    def update_movie_description(self, movie_id, value):
        """
        Updating a movie's description by id
        :param movie_id: movie's id of which title is updated - string
        :param value: value to which the description is updated - string
        :return:
        """
        initial_value = self.movie_repo.find_movie(movie_id).description
        op = Operation(FunctionCall(self.movie_repo.update_movie_description, movie_id, initial_value),
                       FunctionCall(self.movie_repo.update_movie_description, movie_id, value))
        self.undo_service.record(op)
        self.movie_repo.update_movie_description(movie_id, value)

    def update_movie_genre(self, movie_id, value):
        """
        Updating a movie's genre by id
        :param movie_id: movie's id of which genre is updated - string
        :param value: value to which the genre is updated - string
        :return:
        """
        initial_value = self.movie_repo.find_movie(movie_id).genre
        op = Operation(FunctionCall(self.movie_repo.update_movie_genre, movie_id, initial_value),
                       FunctionCall(self.movie_repo.update_movie_genre, movie_id, value))
        self.undo_service.record(op)
        self.movie_repo.update_movie_genre(movie_id, value)


class TestMovieService(unittest.TestCase):
    def setUp(self):
        self.ms = MovieService()
        self.ms.movie_repo.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        self.ms.client_repo.add_client(Client('213', 'Mirel', True))
        self.ms.rental_repo.add_rental(Rental('566', '213', date(2,2,2), date(2,2,10), date(2,2,9)))

    def test_remove_movie(self):
        self.ms.remove_movie('566')
        self.assertEqual(len(self.ms.movie_repo.list), 0)
        self.ms.undo_service.undo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').title, 'Cars')
        self.ms.undo_service.redo()
        self.assertEqual(len(self.ms.movie_repo.list), 0)
        self.assertEqual(len(self.ms.rental_repo.list), 0)

    def test_add_movie(self):
        self.ms.add_movie(Movie('1', 'a', 'a', 'a'))
        self.assertEqual(len(self.ms.movie_repo.list), 2)
        self.ms.undo_service.undo()
        self.assertEqual(len(self.ms.movie_repo.list), 1)
        self.ms.undo_service.redo()
        self.assertEqual(len(self.ms.movie_repo.list), 2)

    def test_update_movie_title(self):
        self.ms.update_movie_title('566', 'a')
        self.assertEqual(self.ms.movie_repo.find_movie('566').title, 'a')
        self.ms.undo_service.undo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').title, 'Cars')
        self.ms.undo_service.redo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').title, 'a')

    def test_update_movie_description(self):
        self.ms.update_movie_description('566', 'a')
        self.assertEqual(self.ms.movie_repo.find_movie('566').description, 'a')
        self.ms.undo_service.undo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').description, 'LIFE')
        self.ms.undo_service.redo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').description, 'a')

    def test_update_movie_genre(self):
        self.ms.update_movie_genre('566', 'a')
        self.assertEqual(self.ms.movie_repo.find_movie('566').genre, 'a')
        self.ms.undo_service.undo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').genre, 'animation, adventure')
        self.ms.undo_service.redo()
        self.assertEqual(self.ms.movie_repo.find_movie('566').genre, 'a')