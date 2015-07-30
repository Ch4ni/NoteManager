from Storage import Storage

class FilesystemStorage(Storage):
    def search(self, searchParam=""):
        pass

    def addNote(self, title="", body=""):
        pass

    def hasNote(self, title=""):
        pass

    class Factory:
        def create(self, *args, **kwargs):
            return FilesystemStorage();
