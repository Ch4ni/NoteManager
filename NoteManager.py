__author__ = 'acripps'

class NoteManager:
    def __init__(self):
        self.notes = {}

    def search(self, searchParam=""):
        if self.notes.has_key(searchParam):
            return {searchParam : self.notes[searchParam]}
        else:
            return {s: self.notes[s] for s in self.getListOfKeysContainingSearchString(searchParam)}

    def getListOfKeysContainingSearchString(self, searchStr):
        return [s for s in self.notes.keys() if searchStr in s]

    def addNote(self, title="", body=""):
        if body == "":
            if title == "":
                raise EmptyNoteException
            raise EmptyBodyException
        if title == "":
            raise EmptyTitleException
        if self.notes.has_key(title):
            raise DuplicateEntryException
        self.notes[title] = body


class EmptyNoteException(Exception):
    pass

class EmptyTitleException(Exception):
    pass

class EmptyBodyException(Exception):
    pass

class DuplicateEntryException(Exception):
    pass
