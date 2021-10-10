class Movie:
    """
    The Movie class
    Attributes:
        id: string
        title: string
        description: string
        genre: string
    """
    def __init__(self, id='', title='', description='', genre=''):
        self._id = id
        self._title = title
        self._description = description
        self._genre = genre

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        self._genre = genre

    def __str__(self):
        txt = self.id + ' ' + self.title + ' ' + self.description + ' ' + self.genre
        return txt
