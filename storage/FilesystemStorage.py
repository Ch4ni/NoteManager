import os
import shutil

from base64 import urlsafe_b64encode,urlsafe_b64decode
from Storage import Storage


class FilesystemStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.base_path = kwargs['base_path']

    def search(self, search_param=""):
        self.__check_basepath_exists()
        if search_param == "":
            return {}
        filenames = [
                urlsafe_b64decode(t)
                for t in os.listdir(self.base_path)
                if search_param in urlsafe_b64decode(t)
        ]
        return {f : self.__get_note_contents(f) for f in filenames}

    def __get_note_contents(self, title):
        self.__check_basepath_exists()
        f = open(self.__get_full_note_path(title), "r")
        note_body = ''.join(f.readlines())
        f.close()
        return note_body

    def add_note(self, title="", body=""):
        self.__check_basepath_exists()
        output = open(self.__get_full_note_path(title), "w")
        output.write(body)
        output.close()

    def __get_full_note_path(self, title=""):
        """ We use bencoding to ensure a filesystem safe hash to use as a
            filename, that is fully reversible.
        """
        return os.path.join(self.base_path, urlsafe_b64encode(title))

    def has_note(self, title=""):
        self.__check_basepath_exists()
        return os.path.exists(
                os.path.join(self.base_path, urlsafe_b64encode(title))
        )

    def _purge_all_notes(self):
        self.__check_basepath_exists()
        shutil.rmtree(self.base_path)

    def __check_basepath_exists(self):
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)


    class Factory:
        def create(self, *args, **kwargs):
            return FilesystemStorage(*args, **kwargs)
