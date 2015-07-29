from DictStorage import DictStorage

class StorageFactory:
    factories = {}
    def createStorage(id):
        if not StorageFactory.factories.has_key(id):
            StorageFactory.factories[id] = eval(id + '.Factory()')
        return StorageFactory.factories[id].create()
    createStorage = staticmethod(createStorage)
