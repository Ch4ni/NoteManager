__author__ = 'acripps'

from storage import StorageFactory
from Note import Note


class NoteManager:
    def __init__(self, storage_type="", *args, **kwargs):
        self.storage = StorageFactory.create_storage(storage_type, *args, **kwargs)

    def search(self, search_param=""):
        return self.storage.search(search_param)

    def add_note(self, title="", body=""):
        note = Note(id, title, body)
        self.validate_note(note)
        self.storage.add_note(note)

    def validate_note(self, note=Note(0,"","")):
        if self.is_empty_note(note):
            raise EmptyNoteException
        if note.title == "":
            raise EmptyTitleException
        if note.body == "":
            raise EmptyBodyException
        if self.storage.has_note(note.title):
            raise DuplicateEntryException

    @staticmethod
    def is_empty_note(note):
        return note.body == "" and note.title == ""

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
