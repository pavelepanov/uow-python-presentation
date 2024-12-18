from typing import Protocol, TypeVar

ModelT = TypeVar('ModelT')


class DataMapper(Protocol[ModelT]):
    """Class used by UoW to send changes to a database"""

    def insert(self, model: ModelT):
        raise NotImplementedError

    def delete(self, model: ModelT):
        raise NotImplementedError

    def update(self, model: ModelT):
        raise NotImplementedError


class UoWModel:
    """
    Model wrapper which allows to implicitly mark model
    as modified on attribute assignment.
    """

    def __init__(self, model, uow):
        self.__dict__['_model'] = model
        self.__dict__['_uow'] = uow

    def __getattr__(self, key):
        return getattr(self._model, key)

    def __setattr__(self, key, value):
        setattr(self._model, key, value)
        self._uow.register_dirty(self._model)


class UnitOfWork:
    def __init__(self):
        self.dirty = dict()
        self.new = dict()
        self.deleted = dict()
        self.mappers = dict()

    def register_dirty(self, model):
        model_id = id(model)
        if model_id in self.new:
            return
        self.dirty[model_id] = model

    def register_deleted(self, model):
        if isinstance(model, UoWModel):
            model = model._model

        model_id = id(model)
        if model_id in self.new:
            self.new.pop(model_id)
            return
        self.deleted[model_id] = model

    def register_new(self, model):
        model_id = id(model)
        self.new[model_id] = model
        return UoWModel(model, self)

    def commit(self):
        for model in self.new.values():
            self.mappers[type(model)].insert(model)
        for model in self.dirty.values():
            self.mappers[type(model)].update(model)
        for model in self.deleted.values():
            self.mappers[type(model)].delete(model)
