__author__ = 'acripps'

class SQLManager:
    def __init__(self):
        self.queries = {}

    def search(self, searchParam=""):
        if self.queries.has_key(searchParam):
            return {searchParam : self.queries[searchParam]}
        else:
            return {s: self.queries[s] for s in self.getListOfKeysContainingSearchString(searchParam)}

    def getListOfKeysContainingSearchString(self, searchStr):
        return [s for s in self.queries.keys() if searchStr in s]

    def addQuery(self, title="", sql=""):
        if sql == "":
            if title == "":
                raise EmptyQueryException
            raise EmptySqlException
        if title == "":
            raise EmptyTitleException
        if self.queries.has_key(title):
            raise DuplicateEntryException
        self.queries[title] = sql


class EmptyQueryException(Exception):
    pass

class EmptyTitleException(Exception):
    pass

class EmptySqlException(Exception):
    pass

class DuplicateEntryException(Exception):
    pass
