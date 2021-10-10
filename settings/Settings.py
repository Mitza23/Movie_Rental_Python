import configparser


class Settings:
    def __init__(self, file):
        self.file_name = file

    def repository_type(self):
        """
        Gets the repository type
        Returns: type of repo - string

        """
        f = open(self.file_name, "r")
        line = f.readline()
        while len(line) > 0:
            tokens = line.strip().split('=')
            if tokens[0] == 'repository':
                return str(tokens[1])
            line = f.readline()
        f.close()

    def client_file(self):
        """
        Gets the file name for the client repo
        Returns: the name of the file - string

        """
        f = open(self.file_name, "r")
        line = f.readline()
        while len(line) > 0:
            tokens = line.strip().split('=')
            if tokens[0] == 'client_repo':
                return str(tokens[1])
            line = f.readline()
        f.close()

    def movie_file(self):
        """
        Gets the file name for the movie repo
        Returns: the name of the file - string

        """
        f = open(self.file_name, "r")
        line = f.readline()
        while len(line) > 0:
            tokens = line.strip().split('=')
            if tokens[0] == 'movie_repo':
                return str(tokens[1])
            line = f.readline()
        f.close()

    def rental_file(self):
        """
        Gets the file name for the rental repo
        Returns: the name of the file - string

        """
        f = open(self.file_name, "r")
        line = f.readline()
        while len(line) > 0:
            tokens = line.strip().split('=')
            if tokens[0] == 'rental_repo':
                return str(tokens[1])
            line = f.readline()
        f.close()


# s = settings()
# print(s.client_file())


# file_names = {
#     'client_text': 'client_repo_text.txt',
#     'client_binary': 'client_repo_binary.pickle',
#     'movie_text': 'movie_repo_text.txt',
#     'movie_binary': 'movie_repo_binary.pickle',
#     'rental_text': 'rental_repo_text.txt',
#     'rental_binary': 'rental_repo_binary.pickle'
#
# }
#
# settings = {
#     "repository_type": "text", # inmemory / text / binary
#     "client_repo": "client_repo_binary.pickle", # / client_repo_text.txt / client_repo_binary.pickle
#     "movie_repo": "movie_repo_binary.pickle", # / movie_repo_text.txt / movie_repo_binary.pickle
#     "rental_repo": "rental_repo_binary.pickle", # / rental_repo_text.txt / rental_repo_binary.pickle
# }
#
# if settings["repository_type"] == "text":
#     settings['client_repo'] = file_names['client_text']
#     settings['movie_repo'] = file_names['movie_text']
#     settings['rental_repo'] = file_names['rental_text']
#
# elif settings["repository_type"] == "binary":
#     settings['client_repo'] = file_names['client_binary']
#     settings['movie_repo'] = file_names['movie_binary']
#     settings['rental_repo'] = file_names['rental_binary']