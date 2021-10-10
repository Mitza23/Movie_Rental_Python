from unittest import TestCase

from domain.Client import Client
from domain.Movie import Movie
from domain.Rental import Rental
from repository.ClientBase import ClientBase
from repository.MovieCollection import MovieCollection
from repository.RentalHistory import RentalHistory
from service.RentalService import RentalService
from datetime import date


class StatisticsService(RentalService):
    """
    StatisticsService class implements statistics functions
    Attributes:
         RentalService attributes

    Methods:
        most_rented_movies
        most_active_clients
        late_rentals

    """

    def __init__(self, client_base, movie_collection, rental_history):
        super().__init__(client_base, movie_collection, rental_history)

    def most_rented_movies(self):
        """
        This will provide the list of movies, sorted in descending order of the number of days they were rented.
        Returns: list of MovieRentedDays

        """
        movie_dict = {}
        for movie in self.movie_repo.list:
            movie_dict[movie.id] = 0

        for rental in self.rental_repo.list:
            if rental.rented_date is not None:
                key = rental.movie_id
                movie_dict[key] += int((rental.returned_date - rental.rented_date).days)

        result =[]
        for entry in movie_dict:
            result.append(MovieRentedDays(self.movie_repo.find_movie(entry).title, movie_dict[entry]))

        result.sort(key=lambda x: x.rented_days, reverse=True)
        return result

    def most_active_clients(self):
        """
        This will provide the list of clients, sorted in descending order of the number
        of movie rental days they have (e.g. having 2 rented movies for 3 days each counts as 2 x 3 = 6 days).
        Returns: list of MovieRentedDays

        """

        client_dict = {}
        for client in self.client_repo.list:
            client_dict[client.id] = 0

        for rental in self.rental_repo.list:
            if rental.rented_date is not None:
                key = rental.client_id
                client_dict[key] += int((rental.returned_date - rental.rented_date).days)

        result = []
        for key in client_dict:
            result.append(MovieRentedDays(self.client_repo.find_client(key).name, client_dict[key]))
        result.sort(key=lambda x: x.rented_days, reverse=True)
        return result

    def late_rentals(self, today):
        """
        This will provide the list of all the movies that are currently rented, for which the due date for return
        has passed, sorted in descending order of the number of days of delay.
        Arguments:
            today: date from which the delay from due date is calculated - datetime.date
        Returns:

        """
        movie_dict = {}
        for movie in self.movie_repo.list:
            movie_dict[movie.id] = 0

        for rental in self.rental_repo.list:
            if rental.rented_date is not None:
                key = rental.movie_id
                movie_dict[key] += int((today - rental.due_date).days)

        result = []
        for entry in movie_dict:
            result.append(MovieRentedDays(self.movie_repo.find_movie(entry).title, movie_dict[entry]))

        result.sort(key=lambda x: x.rented_days, reverse=True)
        return result


class MovieRentedDays:
    """
    Data Transfer Object for statistics
    """
    def __init__(self, rental_id, rented_days):
        self._rental_id = rental_id
        self._rented_days = rented_days

    @property
    def rental_id(self):
        return self._rental_id

    @property
    def rented_days(self):
        return self._rented_days

    def __str__(self):
        return self.rental_id + ' - ' + str(self.rented_days)


class TestStatisticsService(TestCase):

    def setUp(self):
        cr = ClientBase()
        mr = MovieCollection()
        rr = RentalHistory()
        self.ss = StatisticsService(cr, mr, rr)
        self.ss.movie_repo.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        self.ss.movie_repo.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        self.ss.movie_repo.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        self.ss.movie_repo.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        self.ss.movie_repo.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))

        self.ss.client_repo.add_client(Client('213', 'Mirel'))
        self.ss.client_repo.add_client(Client('520', 'Relu'))
        self.ss.client_repo.add_client(Client('964', 'Dana'))
        self.ss.client_repo.add_client(Client('120', 'Lorin'))
        self.ss.client_repo.add_client(Client('687', 'Marcela'))
        self.ss.client_repo.update_client_name('520', 'Gelu')

        self.ss.rental_repo.add_rental(Rental('123', '213', date(2,2,2), date(2,2,13), date(2,2,15)))
        self.ss.rental_repo.add_rental(Rental('156', '520', date(2,2,2), date(2,2,20), date(2,2,19)))
        self.ss.rental_repo.add_rental(Rental('566', '520', date(2,2,2), date(2,2,20), date(2,2,19)))
        self.ss.rental_repo.add_rental(Rental('021', '687', date(2,2,2), date(2,2,12), date(2,2,28)))
        self.ss.rental_repo.add_rental(Rental('782', '213', date(2, 2, 2), date(2, 2, 20), date(2, 2, 20)))

    def test_most_rented_movies(self):
        result = self.ss.most_rented_movies()
        self.assertEqual(result[0].rental_id, 'Expandables II')

    def test_most_active_client(self):
        result = self.ss.most_active_clients()
        self.assertEqual(result[0].rental_id, 'Gelu')

    def test_late_rentals(self):
        result = self.ss.late_rentals(date(2,3,1))
        self.assertEqual(result[0].rental_id, 'Expandables II')