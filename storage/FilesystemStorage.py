import os
import shutil
import cPickle

from base64 import urlsafe_b64encode,urlsafe_b64decode
from Storage import NoteStorage

pickler = cPickle


class FilesystemStorage(NoteStorage):
    def __init__(self, *args, **kwargs):
        self.base_path = kwargs['base_path']
        self.__metadata_path = os.path.join(self.base_path, ".metadata")
        self.__check_basepath_exists()
        if not os.path.exists(self.__metadata_path):
            with open(self.__metadata_path, "w") as metadata:
                pickler.dump(0, metadata, pickler.HIGHEST_PROTOCOL)

    def __check_basepath_exists(self):
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)

    def search(self, search_param=""):
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
        with open(os.path.join(self.base_path, title), "r") as f:
            return pickler.load(f)

    def add_note(self, note):
        note_id = self.__get_new_note_id()
        note.id = note_id
        with open(self.__get_full_note_path(note.title), "w") as output:
            pickler.dump(note, output, pickler.HIGHEST_PROTOCOL)
        return note_id

    def __get_new_note_id(self):
        last_id = None
        with open(self.__metadata_path, "r") as metadata:
            last_id = pickler.load(metadata)
        last_id += 1
        with open(self.__metadata_path, "w") as metadata:
            pickler.dump(last_id, metadata, pickler.HIGHEST_PROTOCOL)
        return last_id

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

    def delete(self, id=None):
        if id is None: return
        files = os.listdir(self.base_path)
        files.remove(os.path.basename(self.__metadata_path))
        for f in files:
            note_path = os.path.join(self.base_path, f)
            with open(note_path, "r") as note_file:
                note = pickler.load(note_file)
                if note.id == id:
                    note_file.close()
                    os.remove(note_path)
                    return

    def _purge_all_notes(self):
        self.__check_basepath_exists()
        shutil.rmtree(self.base_path)


    class Factory:
        def create(self, *args, **kwargs):
            return FilesystemStorage(*args, **kwargs)
