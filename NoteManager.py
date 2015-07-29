__author__ = 'acripps'

from storage.StorageFactory import StorageFactory

class NoteManager:
    def __init__(self):
        self.storage = StorageFactory.createStorage("DictStorage")

    def search(self, searchParam=""):
        return self.storage.search(searchParam)

    def addNote(self, title="", body=""):
        self.validateNote(title, body)
        self.storage.addNote(title, body)

    def validateNote(self, title="", body=""):
        if self.isEmptyNote(title, body):
            raise EmptyNoteException
        if title == "":
            raise EmptyTitleException
        if body == "":
            raise EmptyBodyException
        if self.storage.hasNote(title):
            raise DuplicateEntryException

    def isEmptyNote(self, title="", body=""):
        return body == "" and title == ""


class EmptyNoteException(Exception):
    pass

class EmptyTitleException(Exception):
    pass

class EmptyBodyException(Exception):
    pass

class DuplicateEntryException(Exception):
    pass
