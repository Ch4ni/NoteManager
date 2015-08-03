from Storage import Storage


class DictStorage(Storage):
    notes = None

    def __init__(self):
        self.notes = []

    def search(self, search_param=""):
        return filter(lambda x: search_param in x.title, self.notes)

    def add_note(self, note):
        self.notes.append(note)

    def has_note(self, title=""):
        return len(filter(lambda x: x.title == title, self.notes)) > 0

    def _purge_all_notes(self):
        self.notes = []

    class Factory:
        def create(self, *args, **kwargs):
            return DictStorage()
