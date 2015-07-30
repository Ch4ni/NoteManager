from Storage import Storage


class DictStorage(Storage):
    notes = None

    def __init__(self):
        self.notes = {}

    def search(self, search_param=""):
        if search_param in self.notes:
            return {search_param: self.notes[search_param]}
        else:
            return {s: self.notes[s] for s in self._get_list_of_keys_containing_search_string(search_param)}

    def _get_list_of_keys_containing_search_string(self, search_str):
        return [s for s in self.notes.keys() if search_str in s]

    def add_note(self, title="", body=""):
        self.notes[title] = body

    def has_note(self, title=""):
        return title in self.notes

    class Factory:
        def create(self, *args, **kwargs):
            return DictStorage()
