"""
Iterable class
"""
from unittest import TestCase
import unittest
from domain.Client import Client


class IterableError(Exception):
    def __init__(self, message):
        self._message = message


class Iterable:
    def __init__(self):
        # self._dict = {}
        self._list = []

    @property
    def list(self):
        return self._list

    def find_item_by_id(self, id):
        for entry in self._list:
            if entry.id == id:
                return entry

        return False

    def append(self, item):
        """
        Adds an item to the list
        Args:
            item: item to be added

        Returns:

        """
        if not self.find_item_by_id(item.id):
            self._list.append(item)

    def __getitem__(self, key):
        # return self._dict[key]
        return self.find_item_by_id(key)

    def __delitem__(self, key):
        # self._dict.pop(key)
        item = self.find_item_by_id(key)
        self._list.remove(item)

    def __setitem__(self, key, value):
        # self._dict[key] = value
        found = False
        for i in range(len(self._list)):
            if self._list[i].id == key:
                self._list[i] = value
                found = True

        # for entry in self._list:
        #     if entry.id == key:
        #         entry = value
        #         found = True
        if not found:
            raise IterableError("Item not found")

    def __iter__(self):
        # return iter(self._dict)
        return self._list.__iter__()

    def __next__(self):
        # return next(self.__iter__())
        return self.__iter__().__next__()

    def __len__(self):
        return len(self._list)

    def sort(self, function):
        """
        Gnome sort
        list: the list to be sorted - iterable
        function: should return true if the first parameter is "smaller" than the second - boolean function
        """
        i = 1
        while i < len(self._list):
            # print(function(self._list[i-1], self._list[i]))
            if i > 0 and not function(self._list[i-1], self._list[i]):
                self._list[i-1], self._list[i] = self._list[i], self._list[i-1]
                i -= 1
            else:
                i += 1

    def filter(self, function):
        """
        Filter function
        Args:
            list: list to be filtered - iterable
            function: function to filter by - boolean function

        Returns:
            list of filtered results from the initial list - list

        """
        result = []
        for item in self._list:
            if function(item):
                result.append(item)
        return result


class TestIterable(unittest.TestCase):
    def setUp(self):
        self.it = Iterable()
        self.it.append(Client('1', 'a'))
        self.it.append(Client('2', 'b'))
        self.it.append(Client('3', 'c'))

    def test_list(self):
        list = self.it.list
        self.assertEqual(list[0], Client('1', 'a'))

    def test__getItem__(self):
        self.assertEqual(self.it['1'], Client('1', 'a'))

    def test__delItem__(self):
        self.it.__delitem__('2')
        self.assertFalse(self.it['2'])

    def test__setItem__(self):
        # print(self.it['2'])
        self.it['2'] = Client('2', 'x')
        # print(self.it['2'])
        self.assertEqual(self.it['2'], Client('2', 'x'))
        with self.assertRaises(IterableError):
            self.it['5'] = 'a'

    def test__iter__(self):
        result = []
        for item in self.it:
            result.append(item)

        self.assertEqual(result[0].name, 'a')
        self.assertEqual(result[1].name, 'b')
        self.assertEqual(result[2].name, 'c')

    def test__next__(self):
        i = iter(self.it)
        next(self.it)
        self.assertEqual(next(i).name, 'a')
        self.assertEqual(next(i).name, 'b')
        self.assertEqual(next(i).name, 'c')

    def test__len__(self):
        self.assertEqual(len(self.it), 3)

    def test_sort(self):
        self.it.append(Client('4', '0'))
        self.it.append(Client('7', 'adfa'))
        self.it.append(Client('9', 'arfhgq '))

        self.it.sort(lambda a, b: a.name <= b.name)

        # for a in self.it:
        #     print(a)

        i = iter(self.it)
        while i:
            try:
                self.assertLess(next(i).name, next(i).name)
            except StopIteration:
                i = False

    def test_filter(self):
        self.it.append(Client('5', 'ab'))
        self.it.append(Client('6', 'abc'))
        self.it.append(Client('7', 'abcd'))
        self.it.append(Client('8', 'abcde'))
        self.it.append(Client('9', 'abd'))
        self.it.append(Client('19', 'abe'))

        result = self.it.filter(lambda a: len(a.name) == 3)
        for r in result:
            self.assertEqual(len(r.name), 3)
