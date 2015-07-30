from Storage import Storage


class FilesystemStorage(Storage):
    def __init__(self):
        pass

    def search(self, search_param=""):
        pass

    def add_note(self, title="", body=""):
        pass

    def has_note(self, title=""):
        pass

    class Factory:
        def create(self, *args, **kwargs):
            return FilesystemStorage();
