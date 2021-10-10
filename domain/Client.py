class Client:
    """
    The Client class
    Attributes:
        id: string
        name: string

    Methods:
        __str__: returns a string denoting the Client
    """
    def __init__(self, id, name, worthy=True):
        self._id = id
        self._name = name
        self._worthy = worthy

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def worthy(self):
        return self._worthy

    @worthy.setter
    def worthy(self, worthy):
        self._worthy = worthy

    def __str__(self):
        txt = self.id + ' ' + self.name
        return txt

    def __eq__(self, other):
        if not isinstance(other, Client):
            raise ValueError("Compared items are not from the same class")
        return self.id == other.id
