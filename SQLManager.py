__author__ = 'acripps'

class SQLManager:
    def __init__(self):
        pass

    def search(self, searchParam=""):
        return {}

    def addQuery(self, title="", sql=""):
        if sql == "":
            if title == "":
                raise EmptyQueryException
            raise EmptySqlException
        if title == "":
            raise EmptyTitleException

class EmptyQueryException(Exception):
    pass

class EmptyTitleException(Exception):
    pass

class EmptySqlException(Exception):
    pass
