from DictStorage import DictStorage

class StorageFactory:
    factories = {}
    @staticmethod
    def createStorage(id, *args, **kwargs):
        if not StorageFactory.factories.has_key(id):
            StorageFactory.factories[id] = eval(id + '.Factory()')
        return StorageFactory.factories[id].create(args, kwargs)
