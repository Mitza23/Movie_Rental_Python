from copy import deepcopy
from unittest import TestCase

from domain.Movie import Movie
from repository.Iterable import Iterable


class MovieCollectionError(Exception):
    def __init__(self, message):
        self._message = message


class MovieCollection:
    """
    The MovieCollection class represents a repository for Movies, the movies that exist at the rental shop
    Attributes:
        list: list of Movie

    Methods:
        add_movie: Adds a new Movie to the list
        remove_movie: Removes the Movie with the given id from the list
        update_movie: Updates the attributes of a Movie in the list
            update_movie_id:
            update_movie_title:
            update_movie_description:
            update_movie_genre:
    """

    def __init__(self, list=None):
        if list is None:
            list = Iterable()
        self._list = list

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, list):
        self._list = deepcopy(list)

    def find_movie(self, id):
        """
        Finds the film with the given id in th list
        Args:
            id: id of the movie - string

        Returns: the movie found - Movie , False if not found

        """
        for movie in self.list:
            if movie.id == id:
                return movie
        return False

    def search_movie_by_id(self, id):
        """
        Finds a list of movies with the given id in their id
        Args:
            id: id of movie - string

        Returns: list of Movie

        """
        result = []
        for movie in self.list:
            if movie.id.find(id) != -1:
                result.append(movie)
        return result

    def search_movie_by_title(self, title):
        """
        Finds a list of movies with the given title in their title
        Args:
            title: id of movie - string

        Returns: list of Movie

        """
        result = []
        for movie in self.list:
            if movie.title.lower().find(title.lower()) != -1:
                result.append(movie)
        return result

    def search_movie_by_description(self, description):
        """
        Finds a list of movies with the given description in their description
        Args:
            description: description of movie - string

        Returns: list of Movie

        """
        result = []
        for movie in self.list:
            if movie.description.lower().find(description.lower()) != -1:
                result.append(movie)
        return result

    def search_movie_by_genre(self, genre):
        """
        Finds a list of movies with the given genre in their genre
        Args:
            genre: genre of movie - string

        Returns: list of Movie

        """
        result = []
        for movie in self.list:
            if movie.genre.lower().find(genre.lower()) != -1:
                result.append(movie)
        return result

    def add_movie(self, movie):
        if not self.find_movie(movie.id):
            self.list.append(movie)
        else:
            raise MovieCollectionError("Movie with given id already exists")

    def remove_movie(self, id):
        movie = self.find_movie(id)
        if isinstance(movie, Movie):
            self.list.remove(movie)
        else:
            raise MovieCollectionError("Movie with given id not found")

    def update_movie_id(self, id, new_id):
        """
        Updates the id of the movie with the new id
        Args:
            id: initial id - string
            new_id: replacement - string

        Returns:
        Raises MovieCollectionError if not found
        """
        movie = self.find_movie(id)
        if isinstance(movie, Movie):
            movie.id = new_id
        else:
            raise MovieCollectionError("Movie with given id not found")

    def update_movie_title(self, id, title):
        """
        Updates the title of the movie with the given id
        Args:
            id: id of the movie - string
            title: replacement title - string

        Returns:
        Raises MovieCollectionError if not found
        """
        movie = self.find_movie(id)
        if isinstance(movie, Movie):
            movie.title = title
        else:
            raise MovieCollectionError("Movie with given id not found")

    def update_movie_description(self, id, description):
        """
        Updates the description of the movie with the given id
        Args:
            id: id of the movie - string
            description: replacement description - string

        Returns:
        Raises MovieCollectionError if not found
        """
        movie = self.find_movie(id)
        if isinstance(movie, Movie):
            movie.description = description
        else:
            raise MovieCollectionError("Movie with given id not found")

    def update_movie_genre(self, id, genre):
        """
        Updates the genre of the movie with the given id
        Args:
            id: id of the movie - string
            genre: replacement genre - string

        Returns:
        Raises MovieCollectionError if not found
        """
        movie = self.find_movie(id)
        if isinstance(movie, Movie):
            movie.genre = genre
        else:
            raise MovieCollectionError("Movie with given id not found")


class TestMovieCollection(TestCase):

    def setUp(self):
        self.mc = MovieCollection()
        self.mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        self.mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        self.mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        self.mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        self.mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))

    def test_find_movie(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        mov = self.mc.find_movie('566')
        self.assertEqual(mov.title, 'Cars')
        mov = mc.find_movie('566')
        self.assertEqual(mov.title, 'Cars')

    def test_add_movie(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        with self.assertRaises(MovieCollectionError):
            mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))

    def test_remove_movie(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        mc.remove_movie('123')
        self.assertFalse(mc.find_movie('123'))


    def test_update_movie_id(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        mc.update_movie_id('123', '124')
        self.assertEqual(mc.find_movie('124').title, 'Expandables')

    def test_update_movie_title(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        mc.update_movie_title('566', 'Cars 2')
        mov = mc.find_movie('566')
        self.assertEqual(mov.title, 'Cars 2')

    def test_update_movie_description(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        mc.update_movie_description('566', 'best ever')
        mov = mc.find_movie('566')
        self.assertEqual(mov.description, 'best ever')

    def test_update_movie_genre(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        mc.update_movie_genre('566', 'best ever')
        mov = mc.find_movie('566')
        self.assertEqual(mov.genre, 'best ever')

    def test_search_movie_by_id(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        result = mc.search_movie_by_id('6')
        self.assertEqual(len(result), 2)

    def test_search_movie_by_title(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        result = mc.search_movie_by_title('R')
        self.assertEqual(len(result), 2)

    def test_search_movie_by_description(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        result = mc.search_movie_by_description('o')
        self.assertEqual(len(result), 4)

    def test_search_movie_by_genre(self):
        mc = MovieCollection()
        mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))
        result = mc.search_movie_by_genre('ct')
        self.assertEqual(len(result), 4)

# test_find_movie()
# test_add_movie()
# test_remove_movie()
# test_update_movie_genre()
