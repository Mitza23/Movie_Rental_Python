"""
The RentalHistory class is a repository for movie rentals
"""
from datetime import date
from unittest import TestCase

from domain.Rental import Rental
from repository.RentalHistory import RentalHistory, RentalHistoryError


class RentalHistoryText(RentalHistory):
    """
    The RentalHistory class is a repository for movie rentals
    Attributes:
        list: list of movie rentals - list of Rental

    Methods:
         add_rental: adds a new Rental to the list

    """
    def __init__(self, file):
        super().__init__()
        self._file_name = file

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, list):
        self._list = list[:]

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @staticmethod
    def string_to_date(string):
        """
        Converts a string denoting a date into a Date
        Args:
            string: string to be converted into a Date - string

        Returns: Date that has been converted - Date

        """
        params = string.strip().split('-')
        year = int(params[0])
        month = int(params[1])
        day = int(params[2])
        d = date(year, month, day)
        return d

    def string_to_obj(self, string):
        """
        Converts a string from the auxiliary file to a Rental
        Args:
            string: string in file - string

        Returns: the Rental stored in the string - Rental

        """
        attributes = string.strip().split(';')
        if len(attributes) == 6:
            d1 = self.string_to_date(attributes[3].strip())
            d2 = self.string_to_date(attributes[4].strip())
            d3 = self.string_to_date(attributes[5].strip())
            rental = Rental(attributes[1].strip(), attributes[2].strip(), d1, d2, d3)
        else:
            d1 = self.string_to_date(attributes[3].strip())
            d2 = self.string_to_date(attributes[4].strip())
            rental = Rental(attributes[1].strip(), attributes[2].strip(), d1, d2)
        
        return rental

    @staticmethod
    def obj_to_string(rental):
        """
        Converts a Rental into a string suitable for storing into the file
        Args:
            rental: rental to be parsed - Rental

        Returns: string denoting the Rental - string

        """
        string = rental.id + ';' + rental.movie_id + ';' + rental.client_id + ';' \
              + str(rental.rented_date) + ';' + str(rental.due_date) + ';' + str(rental.returned_date) + '\n'
        return string

    def load_file(self):
        """
        Loads into the repo the data found in the auxiliary file
        Returns:

        """
        try:
            f = open(self._file_name, "r")
            line = f.readline()
            while len(line) > 0:
                super(RentalHistoryText, self).add_rental(self.string_to_obj(line))
                line = f.readline()
            f.close()
        except IOError as e:
            raise e

    def save_file(self):
        """
        Saves into the auxiliary file the current state of the repo
        Returns:

        """
        f = open(self._file_name, "w")
        try:
            for rental in self.list:
                rental_str = self.obj_to_string(rental)
                f.write(rental_str)
            f.close()
        except Exception as e:
            raise e

    def find_rental_by_id(self, id):
        """
        Finds a rental by id in the list
        Args:
            id: the id to search by - string

        Returns: the rental found - Rental or False if not found

        """
        return super(RentalHistoryText, self).find_rental_by_id(id)

    def update_rental_returned_date(self, rental_id, returned_date):
        """
        Updates the returned date fot the rental with the given id
        :param rental_id: id of the rental - string
        :param returned_date: the updated date - date
        :return:
        """
        super(RentalHistoryText, self).update_rental_returned_date(rental_id, returned_date)
        self.save_file()

    def add_rental(self, rental):
        """
        Adds a rental to the list
        Args:
            rental: Rental

        Returns:
        Raises RentalHistoryError if rental already found

        """
        super(RentalHistoryText, self).add_rental(rental)
        self.save_file()

    def remove_rental(self, id):
        """
        Removes a rental from the list
        Args:
            id: id of the rental to be removed - string

        Returns:

        """
        super(RentalHistoryText, self).remove_rental(id)
        self.save_file()


class TestRentalHistory(TestCase):

    def setUp(self):
        self.rh = RentalHistoryText()
        self.rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))
        self.rh.add_rental(Rental('2', '423', date(2002, 2, 17), date(2002, 4, 17), date(2002, 3, 29)))

    def test_load_file(self):
        f = open(self.rh._file_name, "w")
        id1 = str('1' + '2' + str(date(2,2,2)) + str(date(2,2,3)))
        id2 = str('3' + '4' + str(date(2,2,2)) + str(date(2,2,3)))
        id3 = str('3' + '5' + str(date(2,2,2)) + str(date(2,2,3)))
        l1 = id1 + ' ; 1 ; 2 ; date(2, 2, 2) ; date(2, 2, 3) ; date(2, 2, 3) \n'
        l2 = id2 + ' ; 3 ; 4 ; date(2, 2, 2) ; date(2, 2, 3) \n'
        l3 = id3 + ' ; 3 ; 5 ; date(2, 2, 2) ; date(2, 2, 3) ; date(2, 2, 3) \n'
        # tokens = l2.strip().split(';')
        # for t in tokens:
        #     print('->', t.strip())
        f.write(l1)
        f.write(l2)
        f.write(l3)
        f.close()
        self.rh.load_file()
        for r in self.rh.list:
            print('-> ', r.id)
        self.assertEqual(self.rh.find_rental_by_id(id1).returned_date, date(2,2,3))

    def test_add_rental(self):
        with self.assertRaises(RentalHistoryError):
            self.rh.add_rental(Rental('245', '4243', date(2002, 2, 23), date(2002, 4, 23), date(2002, 3, 23)))

    def test_update_rental_returned_date(self):
        id = '245' + '4243' + str(date(2002, 2, 23)) + str(date(2002, 4, 23))
        self.rh.update_rental_returned_date(id, date(2002, 5, 3))
        rental = self.rh.find_rental_by_id(id)
        self.assertEqual(rental.returned_date, date(2002, 5, 3))
        rental.due_date = date(2002, 5, 3)
        self.assertEqual(rental.due_date, date(2002, 5, 3))
        rental.rented_date = date(2002, 2, 3)
        self.assertEqual(rental.rented_date, date(2002, 2, 3))
        rental.client_id = '1'
        self.assertEqual(rental.client_id, '1')
        rental_str = str(rental)

    def test_remove_rental(self):
        id = '245' + '4243' + str(date(2002, 2, 23)) + str(date(2002, 4, 23))
        self.rh.remove_rental(id)
        rental = self.rh.find_rental_by_id(id)
        self.assertFalse(rental)
        self.assertEqual(len(self.rh.list), 1)

    def test_find_rental_by_id(self):
        id = '245' + '4243' + str(date(2002, 2, 23)) + str(date(2002, 4, 23))
        rental = self.rh.find_rental_by_id(id)
        self.assertEqual(rental.rented_date, date(2002, 2, 23))
