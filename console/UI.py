"""
The UI class
"""
from random import randint
from domain.Rental import RentalError
from repository.ClientBaseBinary import ClientBaseBinary
from repository.ClientBaseText import ClientBaseText
from repository.MovieCollection import MovieCollectionError
from repository.MovieCollectionBinary import MovieCollectionBinary
from repository.MovieCollectionText import MovieCollectionText
from repository.RentalHistoryBinary import RentalHistoryBinary
from repository.RentalHistoryText import RentalHistoryText
from service.ClientService import ClientService
from service.MovieService import MovieService
from service.RentalService import *
from service.StatisticsService import StatisticsService
from service.UndoService import UndoService, UndoServiceError
from settings.Settings import Settings


class UIError(Exception):
    def __init__(self, message):
        super().__init__(message)


class UI:
    """
    UI class for interaction with user

    Attributes:
        rental_service: RentalService

    Methods:
        add_client_ui
        remove_client_ui
        update_client_ui
        list_clients
        add_movie_ui
        remove_movie_ui
        update_movie_ui
        list_movies
        rent_movie_ui
        return_movie_ui
        list_rentals
        most_rented_movies_ui
        most_active_clients_ui
        late_rentals_ui
        undo_ui
        redo_ui


    """
    def __init__(self):
        s = Settings('../settings/settings.properties')
        self.repo_type = s.repository_type()
        if self.repo_type == 'inmemory':
            client_repo = ClientBase()
            movie_repo = MovieCollection()
            rental_repo = RentalHistory()

        elif self.repo_type == 'text':
            client_repo = ClientBaseText(s.client_file())
            movie_repo = MovieCollectionText(s.movie_file())
            rental_repo = RentalHistoryText(s.rental_file())

        elif self.repo_type == 'binary':
            client_repo = ClientBaseBinary(s.client_file())
            movie_repo = MovieCollectionBinary(s.movie_file())
            rental_repo = RentalHistoryBinary(s.rental_file())

        undo_service = UndoService()
        self._undo_service = undo_service
        self._rental_service = RentalService(client_repo, movie_repo, rental_repo, undo_service)
        self._client_service = ClientService(client_repo, movie_repo, rental_repo, undo_service)
        self._movie_service = MovieService(client_repo, movie_repo, rental_repo, undo_service)
        self._statistics = StatisticsService(client_repo, movie_repo, rental_repo)


    @property
    def rental_service(self):
        return self._rental_service

    @property
    def client_service(self):
        return self._client_service

    @property
    def movie_service(self):
        return self._movie_service

    @property
    def statistics(self):
        return self._statistics

    @property
    def undo_service(self):
        return self._undo_service

    @staticmethod
    def print_menu():
        print('1. Client options')
        print('2. Movie options')
        print('3. Rent movie')
        print('4. Return movie')
        print('5. List rentals')
        print('6. Statistics')
        print('7. Undo')
        print('8. Redo')
        print('0. Exit')

    @staticmethod
    def print_client_menu():
        print('1. Add client')
        print('2. Remove client')
        print('3. List clients')
        print('4. Update client name')
        print('5. Update client worthiness')
        print('6. Search client by id')
        print('7. Search client by name')
        print('8. Sort client by id')
        print('9. Sort client by name')

    @staticmethod
    def print_movie_menu():
        print('1. Add movie')
        print('2. Remove movie')
        print('3. List movies')
        print('4. Update movie title')
        print('5. Update movie description')
        print('6. Update movie genre')
        print('7. Search movie by id')
        print('8. Search movie by title')
        print('9. Search movie by description')
        print('0.Search movie by genre')
        print('A.Sort movie by id')
        print('B.Sort movie by title')
        print('C.Sort movie by description')
        print('D.Sort movie by genre')

    @staticmethod
    def print_statistics_menu():
        print("1. Most rented movies")
        print("2. Most active clients")
        print("3. Late rentals")

    def client_options(self):
        self.print_client_menu()
        nr = input("What is your wish for clients? ")
        nr = nr.strip()
        if nr.isnumeric():
            nr = int(nr)
            if 1 <= nr <= 9:
                if nr == 1:
                    self.add_client_ui()
                elif nr == 2:
                    self.remove_client_ui()
                elif nr == 3:
                    self.list_clients()
                elif nr == 4:
                    self.update_client_name()
                elif nr == 5:
                    self.update_client_worthiness()
                elif nr == 6:
                    self.search_client_by_id_ui()
                elif nr == 7:
                    self.search_client_by_name_ui()
                elif nr == 8:
                    self.sort_clients_by_id_ui()
                elif nr == 9:
                    self.sort_clients_by_name_ui()
            else:
                raise UIError("Your wish doesn't exist")
        else:
            raise UIError("Your wish must be a number")

    def add_client_ui(self):
        id = input("Client ID: ")
        name = input("Client name: ")
        self.client_service.add_client(Client(id.strip(), name.strip()))

    def remove_client_ui(self):
        id = input("Client ID: ").strip()
        ok = True
        for rt in self.rental_service.rental_repo.list:
            if rt.client_id == id and rt.returned_date is None:
                ok = False
        if not ok:
            raise RentalServiceError("Client can't be removed as it has a rental in process")
        else:
            self.client_service.remove_client(id)

    def list_clients(self):
        for client in self.rental_service.client_repo.list:
            print(client.__str__())

    def update_client_name(self):
        id = input("Client ID: ")
        name = input("Client name: ")
        self.client_service.update_client_name(id.strip(), name.strip())

    def update_client_worthiness(self):
        id = input("Client ID: ")
        worthy = input("yes/no: ")
        id = id.strip()
        worthy = worthy.strip()
        if worthy == 'no':
            self.client_service.update_client_worthy(id, False)
        elif worthy == 'yes':
            self.client_service.update_client_worthy(id, True)
        else:
            raise UIError("Worthiness should be either 'yes' or 'no'")

    def search_client_by_id_ui(self):
        id = input("Client ID: ").strip()
        # result = self.rental_service.client_repo.search_client_by_id(id)
        result = self.rental_service.client_repo.list.filter(lambda x: x.id.find(id) != -1)
        if len(result) == 0:
            raise ClientBaseError("Clients can't be found")
        else:
            for client in result:
                print(str(client))

    def search_client_by_name_ui(self):
        name = input("Client name: ").strip().lower()
        # result = self.rental_service.client_repo.search_client_by_name(name)
        result = self.rental_service.client_repo.list.filter(lambda x: x.name.lower().find(name) != -1)
        if len(result) == 0:
            raise ClientBaseError("Clients can't be found")
        else:
            for client in result:
                print(str(client))

    def sort_clients_by_id_ui(self):
        self.client_service.client_repo.list.sort(lambda a, b: int(a.id) <= int(b.id))

    def sort_clients_by_name_ui(self):
        self.client_service.client_repo.list.sort(lambda a, b: str(a.name).lower() <= str(b.name).lower())

    def movie_options(self):
        self.print_movie_menu()
        nr = input("What is your wish for movies? ")
        nr = nr.strip()
        if nr.isalnum():
            if nr.isnumeric():
                nr = int(nr)
                if 0 <= nr <= 9:
                    if nr == 1:
                        self.add_movie_ui()
                    if nr == 2:
                        self.remove_movie_ui()
                    if nr == 3:
                        self.list_movies()
                    if nr == 4:
                        self.update_movie_title()
                    if nr == 5:
                        self.update_movie_description()
                    if nr == 6:
                        self.update_movie_genre()
                    if nr == 7:
                        self.search_movie_by_id_ui()
                    if nr == 8:
                        self.search_movie_by_title_ui()
                    if nr == 9:
                        self.search_movie_by_description_ui()
                    if nr == 0:
                        self.search_movie_by_genre_ui()

                else:
                    raise UIError("Your wish doesn't exist")

            elif nr.isalpha():
                nr = nr.upper()
                if nr == 'A':
                    self.sort_movie_by_id()
                elif nr == 'B':
                    self.sort_movie_by_title()
                elif nr == 'C':
                    self.sort_movie_by_description()
                elif nr == 'D':
                    self.sort_movie_by_genre()

                else:
                    raise UIError("Your wish doesn't exist")

        else:
            raise UIError("Your wish must be a number or a letter")

    def add_movie_ui(self):
        id = input("Movie ID: ").strip()
        title = input("Movie title: ").strip()
        description = input("Movie description: ").strip()
        genre = input("Movie genre: ").strip()
        self.movie_service.add_movie(Movie(id, title, description, genre))

    def remove_movie_ui(self):
        id = input("Movie ID: ").strip()
        # year = int(input("Removal date year: ").strip())
        # month = int(input("Removal date month: ").strip())
        # day = int(input("o date month: ").strip())
        # removal_date = date(year, month, day)
        # if self.rental_service.is_movie_available(id, removal_date):
        self.movie_service.remove_movie(id)
        # else:
        #     raise RentalServiceError("Movie can't be removed as it's rented")

    def list_movies(self):
        for movie in self.rental_service.movie_repo.list:
            print(str(movie))

    def update_movie_title(self):
        id = input("Movie ID: ").strip()
        title = input("Movie title: ").strip()
        self.movie_service.update_movie_title(id, title)

    def update_movie_description(self):
        id = input("Movie ID: ").strip()
        description = input("Movie description: ").strip()
        self.movie_service.update_movie_genre(description)

    def update_movie_genre(self):
        id = input("Movie ID: ").strip()
        genre = input("Movie genre: ").strip()
        self.movie_service.update_movie_genre(id, genre)

    def search_movie_by_id_ui(self):
        id = input("Movie ID: ").strip()
        # result = self.rental_service.movie_repo.search_movie_by_id(id)
        result = self.rental_service.movie_repo.list.filter(lambda x: x.id.find(id) != -1)
        if len(result) == 0:
            raise ClientBaseError("Movies can't be found")
        else:
            for movie in result:
                print(str(movie))

    def search_movie_by_title_ui(self):
        title = input("Movie title: ").strip().lower()
        # result = self.rental_service.movie_repo.search_movie_by_title(title)
        result = self.rental_service.movie_repo.list.filter(lambda x: x.title.lower().find(title) != -1)
        if len(result) == 0:
            raise ClientBaseError("Movies can't be found")
        else:
            for movie in result:
                print(str(movie))

    def search_movie_by_description_ui(self):
        description = input("Movie description: ").strip().lower()
        # result = self.rental_service.movie_repo.search_movie_by_description(description)
        result = self.rental_service.movie_repo.list.filter(lambda x: x.description.lower().find(description) != -1)
        if len(result) == 0:
            raise ClientBaseError("Movies can't be found")
        else:
            for movie in result:
                print(str(movie))

    def search_movie_by_genre_ui(self):
        genre = input("Movie genre: ").strip().lower()
        # result = self.rental_service.movie_repo.search_movie_by_genre(genre)
        result = self.rental_service.movie_repo.list.filter(lambda x: x.genre.lower().find(genre) != -1)
        if len(result) == 0:
            raise ClientBaseError("Movies can't be found")
        else:
            for movie in result:
                print(str(movie))

    def sort_movie_by_id(self):
        self.movie_service.movie_repo.list.sort(lambda a, b: int(a.id) <= int(b.id))

    def sort_movie_by_title(self):
        self.movie_service.movie_repo.list.sort(lambda a, b: str(a.title).lower() <= str(b.title).lower())

    def sort_movie_by_description(self):
        self.movie_service.movie_repo.list.sort(lambda a, b: str(a.description).lower() <= str(b.description).lower())

    def sort_movie_by_genre(self):
        self.movie_service.movie_repo.list.sort(lambda a, b: str(a.genre).lower() <= str(b.genre).lower())

    def statistics_ui(self):
        self.print_statistics_menu()
        nr = input("What is your wish for statistics? ")
        nr = nr.strip()
        if nr.isnumeric():
            nr = int(nr)
            if 1 <= nr <= 3:
                if nr == 1:
                    self.most_rented_movies_ui()
                if nr == 2:
                    self.most_active_clients_ui()
                if nr == 3:
                    self.late_rentals_ui()
            else:
                raise UIError("Your wish doesn't exist")

        else:
            raise UIError("Your wish must be a number")

    def most_rented_movies_ui(self):
        result = self.statistics.most_rented_movies()
        if len(result) == 0:
            raise RentalServiceError("No rentals done")
        for entry in result:
            print(str(entry))

    def most_active_clients_ui(self):
        result = self.statistics.most_active_clients()
        if len(result) == 0:
            raise RentalServiceError("No rentals done")
        for entry in result:
            print(str(entry))

    def late_rentals_ui(self):
        year = int(input("Today date year: ").strip())
        month = int(input("Today date month: ").strip())
        day = int(input("Today date month: ").strip())
        today = date(year, month, day)
        result = self.statistics.late_rentals(today)
        if len(result) == 0:
            raise RentalServiceError("No rentals done")
        for entry in result:
            print(str(entry))


    def rent_movie_ui(self):
        movie_id = input("Movie ID: ").strip()
        client_id = input("Client ID: ").strip()

        year = int(input("Rented date year: ").strip())
        month = int(input("Rented date month: ").strip())
        day = int(input("Rented date month: ").strip())
        rented_date = date(year, month, day)

        year = int(input("Due date year: ").strip())
        month = int(input("Due date month: ").strip())
        day = int(input("Due date month: ").strip())
        due_date = date(year, month, day)

        self.rental_service.rent_movie(movie_id, client_id, rented_date, due_date)

    def return_movie_ui(self):
        movie_id = input("Movie ID: ").strip()
        client_id = input("Client ID: ").strip()

        year = int(input("Rented date year: ").strip())
        month = int(input("Rented date month: ").strip())
        day = int(input("Rented date month: ").strip())
        rented_date = date(year, month, day)

        year = int(input("Due date year: ").strip())
        month = int(input("Due date month: ").strip())
        day = int(input("Due date month: ").strip())
        due_date = date(year, month, day)

        year = int(input("Returned date year: ").strip())
        month = int(input("Returned date month: ").strip())
        day = int(input("Returned date month: ").strip())
        returned_date = date(year, month, day)

        self.rental_service.return_movie(movie_id, client_id, rented_date, due_date, returned_date)

    def list_rentals(self):
        for rental in self.rental_service.rental_repo.list:
            print(str(rental))

    def undo_ui(self):
        self.undo_service.undo()

    def redo_ui(self):
        self.undo_service.redo()

    def start(self):
        if self.repo_type == 'inmemory':
            self.generate_clients()
            self.generate_movies()
            self.generate_rentals()
        else:
            try:
                self.client_service.client_repo.load_file()
                self.movie_service.movie_repo.load_file()
                self.rental_service.rental_repo.load_file()
            except (EOFError, ClientBaseError, MovieCollectionError, RentalHistoryError) as error:
                print(str(error))
        done = False
        while not done:
            self.print_menu()
            nr = input("What is your wish? ")
            nr = nr.strip()
            if nr.isnumeric():
                nr = int(nr)
                if 0 <= nr <= 8:
                    try:
                        if nr == 1:
                            self.client_options()
                        elif nr == 2:
                            self.movie_options()
                        elif nr == 3:
                            self.rent_movie_ui()
                        elif nr == 4:
                            self.return_movie_ui()
                        elif nr == 5:
                            self.list_rentals()
                        elif nr == 6:
                            self.statistics_ui()
                        elif nr == 7:
                            self.undo_ui()
                        elif nr == 8:
                            self.redo_ui()
                        else:
                            print('See you l8er, alligator!')
                            done = True
                    except (UIError, MovieCollectionError, ClientBaseError, RentalHistoryError, RentalServiceError,
                            RentalError, UndoServiceError) as error:
                        print(str(error))
                else:
                    print("Your wish doesn't exist")
            else:
                print("Your wish must be a number")

    def generate_clients(self):
        client_names = ['Ana', 'Dan', 'Mirel', 'Patricia', 'Maria', 'Vlad', 'Alex', 'Mircea', 'Gabriel', 'Bogdan'
                        , 'Diana', 'Mara']
        for i in range(10):
            name = client_names[randint(0, len(client_names)-1)]
            exist = True
            while exist:
                exist = False
                id = str(randint(1, 100))
                for cl in self.rental_service.client_repo.list:
                    if cl.id == id:
                        exist = True
            self.rental_service.client_repo.add_client(Client(id, name))

    def generate_movies(self):
        movie_names = ['Armageddon', 'Cars', 'Cars 2', 'Cars 3', 'Alien', 'Avatar', 'Avengers', 'Sherlock Holmes',
                       'SpiderMan', 'Black Panther', 'Wolf of WallStreet', 'Mission Impossible', 'Ford vs. Ferrari']
        movie_descriptions = ['terrible', 'average', 'good', 'great', "OH MY F*CKING GOD THAT'S AWESOME"]
        movie_genres = ['animation', 'action', 'adventure', 'romance', 'comedy', 'life', 'BEST MOVIE EVER MADE']
        for i in range(10):
            title = movie_names[randint(0, len(movie_names)-1)]
            description = movie_descriptions[randint(0, len(movie_descriptions)-1)]
            genre = movie_genres[randint(0, len(movie_genres)-1)]
            exist = True
            while exist:
                exist = False
                id = str(randint(1, 100))
                for mv in self.rental_service.movie_repo.list:
                    if mv.id == id:
                        exist = True
            self.rental_service.movie_repo.add_movie(Movie(id, title, description, genre))

    def generate_rentals(self):
        movie_id_list = []
        client_id_list = []
        for item in self.rental_service.movie_repo.list:
            movie_id_list.append(item.id)

        for item in self.rental_service.client_repo.list:
            client_id_list.append(item.id)

        for i in range(10):
            movie_id = movie_id_list[randint(0, 9)]
            client_id = client_id_list[randint(0, 9)]

            day = randint(1,28)
            month = randint(1,12)
            year = randint(1,10)
            rented_date = date(year, month, day)

            day = randint(1, 28)
            month = randint(1, 12)
            year = randint(1, 10)
            due_date = date(year, month, day)

            day = randint(1, 28)
            month = randint(1, 12)
            year = randint(1, 10)
            returned_date = date(year, month, day)

            while rented_date > due_date or rented_date > returned_date:
                day = randint(1, 28)
                month = randint(1, 12)
                year = randint(1, 10)
                rented_date = date(year, month, day)

                day = randint(1, 28)
                month = randint(1, 12)
                year = randint(1, 10)
                due_date = date(year, month, day)

                day = randint(1, 28)
                month = randint(1, 12)
                year = randint(1, 10)
                returned_date = date(year, month, day)

            self.rental_service.rental_repo.add_rental(Rental(movie_id, client_id, rented_date, due_date, returned_date))


# a = Client('1', 'Maraea')
# b = Client('3', 'ADafa')
# c = Client('4', 'Fagfaga')
#
# it = Iterable()
# it.append(a)
# it.append(b)
# it.append(c)
#
# it.sort(lambda x, y: x.name < y.name)
#
# for item in it.list:
#     print(item)

ui = UI()
ui.start()
