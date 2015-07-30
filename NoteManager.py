__author__ = 'acripps'

from storage import StorageFactory


class NoteManager:
    def __init__(self, storage_type=""):
        self.storage = StorageFactory.createStorage(storage_type)

    def search(self, search_param=""):
        return self.storage.search(search_param)

    def add_note(self, title="", body=""):
        self.validate_note(title, body)
        self.storage.add_note(title, body)

    def validate_note(self, title="", body=""):
        if self.is_empty_note(title, body):
            raise EmptyNoteException
        if title == "":
            raise EmptyTitleException
        if body == "":
            raise EmptyBodyException
        if self.storage.has_note(title):
            raise DuplicateEntryException

    @staticmethod
    def is_empty_note(title="", body=""):
        return body == "" and title == ""


class EmptyNoteException(Exception):
    pass


class EmptyTitleException(Exception):
    pass


class EmptyBodyException(Exception):
    pass


class DuplicateEntryException(Exception):
    pass
