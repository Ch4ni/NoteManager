from Storage import NoteStorage


class DictStorage(NoteStorage):
    notes = None
    last_id = None

    def __init__(self):
        self.notes = []
        self.last_id = 0

    def search(self, search_param=""):
        return filter(lambda x: search_param in x.title, self.notes)

    def add_note(self, note):
        self.last_id += 1
        note.id = self.last_id
        self.notes.append(note)
        return self.last_id

    def has_note(self, title=""):
        return len(filter(lambda x: x.title == title, self.notes)) > 0

    def delete(self, id=None):
        self.notes.remove(*filter(lambda x: x.id == id, self.notes))

    def _purge_all_notes(self):
        self.notes = []

    class Factory:
        def create(self, *args, **kwargs):
            return DictStorage()
