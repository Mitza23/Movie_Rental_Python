from datetime import datetime


class RentalError(Exception):
    """
    RentalError class is for errors related to the Rental class
    """
    def __init__(self, message):
        self._message = message


class Rental:
    """
    Rental class
    Attributes:
        id: string
        movie_id: string
        client_id: string
        rented_date: datetime
        due_date: datetime
        returned_date: datetime
    """

    def __init__(self, movie_id, client_id, rented_date, due_date, returned_date=None):
        self._id = movie_id + client_id + str(rented_date) + str(due_date)
        self._movie_id = movie_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._due_date = due_date
        self._returned_date = returned_date

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def movie_id(self):
        return self._movie_id

    @movie_id.setter
    def movie_id(self, movie_id):
        self._movie_id = movie_id

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @property
    def rented_date(self):
        return self._rented_date

    @rented_date.setter
    def rented_date(self, rented_date):
        if self.due_date > rented_date and rented_date < self.returned_date:
            self._rented_date = rented_date
        else:
            raise RentalError("Rented date after due date or returned date")

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        if due_date > self.rented_date:
            self._due_date = due_date
        else:
            raise RentalError("Rented date after due date")

    @property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, returned_date=None):
        if returned_date is None:
            self._returned_date = None
        else:
            if returned_date > self.rented_date:
                self._returned_date = returned_date
            else:
                raise RentalError("Returned date before rented date")

    def __str__(self):
        txt = 'id:' + self.id + ' movie id:' + self.movie_id + ' client id:' + self.client_id + ' ' \
              + str(self.rented_date) + ' ' + str(self.due_date) + ' ' + str(self.returned_date)
        return txt
