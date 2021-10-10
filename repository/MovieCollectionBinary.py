import pickle
from copy import deepcopy
from unittest import TestCase

from domain.Movie import Movie
from repository.MovieCollection import MovieCollection, MovieCollectionError


class MovieCollectionBinary(MovieCollection):
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
        Converts a string from the auxiliary file to a Movie
        Args:
            string: string in file - string

        Returns: the movie stored in the string - Movie

        """
        attributes = string.strip().split(';')
        movie = Movie(attributes[0].strip(), attributes[1].strip(), attributes[2].strip(), attributes[3].strip())
        return movie

    @staticmethod
    def obj_to_string(movie):
        """
        Converts a Movie into a string suitable for storing into the file
        Args:
            movie: movie to be parsed - Movie

        Returns: string denoting the movie - string

        """
        string = movie.id + ' ; ' + movie.title + ' ; ' + movie.description + ' ; ' + movie.genre + '\n'
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
                super(MovieCollectionBinary, self).add_movie(self.string_to_obj(str))
            f.close()
        except EOFError:
            raise MovieCollectionError("Empty binary file")
        except IOError as e:
            raise e

    def save_file(self):
        """
        Saves into the auxiliary file the current state of the repo
        Returns:

        """
        f = open(self._file_name, "wb")
        string_list = []
        for movie in self.list:
            movie_str = self.obj_to_string(movie)
            string_list.append(movie_str)
        pickle.dump(string_list, f)
        f.close()

    def find_movie(self, id):
        """
        Finds the film with the given id in th list
        Args:
            id: id of the movie - string

        Returns: the movie found - Movie , False if not found

        """
        return super(MovieCollectionBinary, self).find_movie(id)

    def search_movie_by_id(self, id):
        """
        Finds a list of movies with the given id in their id
        Args:
            id: id of movie - string

        Returns: list of Movie

        """
        return super(MovieCollectionBinary, self).search_movie_by_id(id)

    def search_movie_by_title(self, title):
        """
        Finds a list of movies with the given title in their title
        Args:
            title: id of movie - string

        Returns: list of Movie

        """
        return super(MovieCollectionBinary, self).search_movie_by_title(title)

    def search_movie_by_description(self, description):
        """
        Finds a list of movies with the given description in their description
        Args:
            description: description of movie - string

        Returns: list of Movie

        """
        return super(MovieCollectionBinary, self).search_movie_by_description(description)

    def search_movie_by_genre(self, genre):
        """
        Finds a list of movies with the given genre in their genre
        Args:
            genre: genre of movie - string

        Returns: list of Movie

        """
        return super(MovieCollectionBinary, self).search_movie_by_genre(genre)

    def add_movie(self, movie):
        super(MovieCollectionBinary, self).add_movie(movie)
        self.save_file()

    def remove_movie(self, id):
        super(MovieCollectionBinary, self).remove_movie(id)
        self.save_file()

    def update_movie_id(self, id, new_id):
        """
        Updates the id of the movie with the new id
        Args:
            id: initial id - string
            new_id: replacement - string

        Returns:
        Raises MovieCollectionError if not found
        """
        super(MovieCollectionBinary, self).update_movie_id(id, new_id)
        self.save_file()

    def update_movie_title(self, id, title):
        """
        Updates the title of the movie with the given id
        Args:
            id: id of the movie - string
            title: replacement title - string

        Returns:
        Raises MovieCollectionError if not found
        """
        super(MovieCollectionBinary, self).update_movie_title(id, title)
        self.save_file()

    def update_movie_description(self, id, description):
        """
        Updates the description of the movie with the given id
        Args:
            id: id of the movie - string
            description: replacement description - string

        Returns:
        Raises MovieCollectionError if not found
        """
        super(MovieCollectionBinary, self).update_movie_description(id, description)
        self.save_file()

    def update_movie_genre(self, id, genre):
        """
        Updates the genre of the movie with the given id
        Args:
            id: id of the movie - string
            genre: replacement genre - string

        Returns:
        Raises MovieCollectionError if not found
        """
        super(MovieCollectionBinary, self).update_movie_genre(id, genre)
        self.save_file()


class TestMovieCollectionBinary(TestCase):
    def setUp(self):
        self.mc = MovieCollectionBinary()
        self.mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))
        self.mc.add_movie(Movie('021', 'Expandables II', 'BOOM', 'action'))
        self.mc.add_movie(Movie('156', 'Expandables III', 'BOOM', 'action'))
        self.mc.add_movie(Movie('566', 'Cars', 'LIFE', 'animation, adventure'))
        self.mc.add_movie(Movie('782', 'Transformers', 'BOOM BOOM BOOM', 'action'))

    def test_find_movie(self):
        mov = self.mc.find_movie('566')
        self.assertEqual(mov.title, 'Cars')

    def test_add_movie(self):
        with self.assertRaises(MovieCollectionError):
            self.mc.add_movie(Movie('123', 'Expandables', 'BOOM', 'action'))

    def test_remove_movie(self):
        self.mc.remove_movie('123')
        self.assertFalse(self.mc.find_movie('123'))

    def test_update_movie_id(self):
        self.mc.update_movie_id('123', '124')
        self.assertEqual(self.mc.find_movie('124').title, 'Expandables')

    def test_update_movie_title(self):
        self.mc.update_movie_title('566', 'Cars 2')
        mov = self.mc.find_movie('566')
        self.assertEqual(mov.title, 'Cars 2')

    def test_update_movie_description(self):
        self.mc.update_movie_description('566', 'best ever')
        mov = self.mc.find_movie('566')
        self.assertEqual(mov.description, 'best ever')

    def test_update_movie_genre(self):
        self.mc.update_movie_genre('566', 'best ever')
        mov = self.mc.find_movie('566')
        self.assertEqual(mov.genre, 'best ever')
