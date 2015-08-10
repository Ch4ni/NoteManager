class NoteStorage:
    def add_note(self, title="", body=""):
        pass
    
    def search(self, search_param=""):
        pass

    def has_note(self, title=""):
        pass

    def delete(self, id=None):
        pass

    def _purge_all_notes(self):
        pass

class NoteDoesNotExistException(Exception):
    pass
