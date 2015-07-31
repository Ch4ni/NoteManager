from DictStorage import DictStorage
from FilesystemStorage import FilesystemStorage


class StorageFactory:
    factories = {}

    def __init__(self):
        pass

    @staticmethod
    def create_storage(id_, *args, **kwargs):
        if not StorageFactory.factories.has_key(id_):
            StorageFactory.factories[id_] = eval(id_ + '.Factory()')
        return StorageFactory.factories[id_].create(*args, **kwargs)
