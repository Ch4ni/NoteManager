import os
import shutil
import cPickle

from base64 import urlsafe_b64encode,urlsafe_b64decode
from Storage import Storage

pickler = cPickle


class FilesystemStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.base_path = kwargs['base_path']

    def search(self, search_param=""):
        self.__check_basepath_exists()
        if search_param == "":
            return []
        filename_title_dict = self.__get_matching_filename_title_dict(search_param)
        return {
                self.__get_note_contents(f)
                for f in filename_title_dict
        }

    def __get_matching_filename_title_dict(self, search_param=""):
        matching_filenames = {}
        for t in os.listdir(self.base_path):
            decoded_filename = urlsafe_b64decode(t)
            if search_param in decoded_filename:
                matching_filenames[t] = decoded_filename
        return matching_filenames

    def __get_note_contents(self, title):
        self.__check_basepath_exists()
        with open(os.path.join(self.base_path, title), "r") as f:
            return pickler.load(f)

    def add_note(self, note):
        self.__check_basepath_exists()
        with open(self.__get_full_note_path(note.title), "w") as output:
            pickler.dump(note, output, pickler.HIGHEST_PROTOCOL)

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
