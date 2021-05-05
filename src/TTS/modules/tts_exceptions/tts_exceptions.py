class WrongPunctuationException(Exception):
    def __init__(self, what):
        self.__what = what

    def what(self):
        return self.__what


class DBConnectionException(Exception):
    def __init__(self, what):
        self.__what = what

    def what(self):
        return self.__what


class LTPNotInitializedExceprion(Exception):
    def __init__(self, what):
        self.__what = what

    def what(self):
        return self.__what
