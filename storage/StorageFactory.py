from DictStorage import DictStorage

class StorageFactory:
    factories = {}
    def createStorage(id, *args, **kwargs):
        if not StorageFactory.factories.has_key(id):
            StorageFactory.factories[id] = eval(id + '.Factory()')
        return StorageFactory.factories[id].create(args, kwargs)
    createStorage = staticmethod(createStorage)
