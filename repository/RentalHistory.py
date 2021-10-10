"""
The RentalHistory class is a repository for movie rentals
"""
from unittest import TestCase

from domain.Rental import Rental
from datetime import date

from repository.Iterable import Iterable


class RentalHistoryError(Exception):
    def __init__(self, message):
        self._message = message


class RentalHistory:
    """
    The RentalHistory class is a repository for movie rentals
    Attributes:
        list: list of movie rentals - list of Rental

    Methods:
         add_rental: adds a new Rental to the list

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
        self._list = list[:]

    def find_rental_by_id(self, id):
        """
        Finds a rental by id in the list
        Args:
            id: the id to search by - string

        Returns: the rental found - Rental or False if not found

        """
        for rental in self.list:
            if rental.id == id:
                return rental
        return False

    def update_rental_returned_date(self, rental_id, returned_date):
        """
        Updates the returned date fot the rental with the given id
        :param rental_id: id of the rental - string
        :param returned_date: the updated date - date
        :return:
        """
        rental = self.find_rental_by_id(rental_id)
        rental.returned_date = returned_date

    def add_rental(self, rental):
        """
        Adds a rental to the list
        Args:
            rental: Rental

        Returns:
        Raises RentalHistoryError if rental already found

        """
        if not self.find_rental_by_id(rental.id):
            self.list.append(rental)
        else:
            raise RentalHistoryError("Rental already found")

    def remove_rental(self, id):
        """
        Removes a rental from the list
        Args:
            id: id of the rental to be removed - string

        Returns:

        """
        rental = self.find_rental_by_id(id)
        if isinstance(rental, Rental):
            self.list.remove(rental)
        else:
            raise RentalHistoryError("Rental not in the list")


class TestRentalHistory(TestCase):

    def test_add_rental(self):
        rh = RentalHistory()
        rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))
        rh.add_rental(Rental('2', '423', date(2002, 2, 17), date(2002, 4, 17), date(2002, 3, 29)))
        with self.assertRaises(RentalHistoryError):
            rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))

    def test_update_rental_returned_date(self):
        rh = RentalHistory()
        rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))
        id = '245' + '4243' + str(date(2002, 2, 23)) + str(date(2002, 4, 23))
        rh.update_rental_returned_date(id, date(2002, 5, 3))
        rental = rh.find_rental_by_id(id)
        self.assertEqual(rental.returned_date, date(2002, 5, 3))
        rental.due_date = date(2002, 5, 3)
        self.assertEqual(rental.due_date, date(2002, 5, 3))
        rental.rented_date = date(2002, 2, 3)
        self.assertEqual(rental.rented_date, date(2002, 2, 3))
        rental.client_id = '1'
        self.assertEqual(rental.client_id, '1')
        rental_str = str(rental)

    def test_remove_rental(self):
        rh = RentalHistory()
        rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))
        rh.add_rental(Rental('2', '423', date(2002, 2, 17), date(2002, 4, 17), date(2002, 3, 29)))
        id = '245' + '4243' + str(date(2002, 2, 23)) + str(date(2002, 4, 23))
        rh.remove_rental(id)
        rental = rh.find_rental_by_id(id)
        self.assertFalse(rental)
        self.assertEqual(len(rh.list), 1)

    def test_find_rental_by_id(self):
        rh = RentalHistory()
        rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))
        rh.add_rental(Rental('2', '423', date(2002, 2, 17), date(2002, 4, 17), date(2002, 3, 29)))
        id = '245' + '4243' + str(date(2002, 2, 23)) + str(date(2002, 4, 23))
        rental = rh.find_rental_by_id(id)
        self.assertEqual(rental.rented_date, date(2002, 2, 23))


# test_find_rental_by_id()
# test_remove_rental()
