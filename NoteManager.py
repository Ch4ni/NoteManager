__author__ = 'acripps'

from storage import StorageFactory


class NoteManager:
    def __init__(self, storage_type="", *args, **kwargs):
        self.storage = StorageFactory.create_storage(storage_type, *args, **kwargs)

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

    def _purge_all_notes(self):
        self.storage._purge_all_notes()


class EmptyNoteException(Exception):
    pass


class EmptyTitleException(Exception):
    pass


class EmptyBodyException(Exception):
    pass


class DuplicateEntryException(Exception):
    pass
