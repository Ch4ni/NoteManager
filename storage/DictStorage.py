from Storage import Storage

class DictStorage(Storage):
    notes = None
    def __init__(self):
        self.notes = {}

    def search(self, searchParam):
        if self.notes.has_key(searchParam):
            return {searchParam : self.notes[searchParam]}
        else:
            return {s: self.notes[s] for s in self._getListOfKeysContainingSearchString(searchParam)}

    def _getListOfKeysContainingSearchString(self, searchStr):
        return [s for s in self.notes.keys() if searchStr in s]

    def addNote(self, title="", body=""):
        self.notes[title] = body

    def hasNote(self, title=""):
        return self.notes.has_key(title)

    class Factory:
        def create(self):
            return DictStorage()
