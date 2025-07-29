from reqdb.api import API
from reqdb.models import (
    Base,
    Catalogue,
    Comment,
    Configuration,
    ExtraEntry,
    ExtraType,
    Requirement,
    Tag,
    Topic,
)


class ReqDB:

    api = None

    def __init__(self, fqdn, bearer, insecure: bool = False) -> None:
        ReqDB.api = API(fqdn, bearer, insecure)

    class Entity:
        endpoint: str = None
        model: Base = None

        @classmethod
        def get(cls, id: int) -> dict|bool:
            return ReqDB.api.get(f"{cls.endpoint}/{id}")

        @classmethod
        def all(cls) -> dict|bool:
            return ReqDB.api.get(f"{cls.endpoint}")

        @classmethod
        def update(cls, id: int, data: Base) -> dict|bool:
            if not isinstance(data, cls.model):
                raise TypeError(f"Data not the correct model ({cls.model.__name__})")
            return ReqDB.api.update(f"{cls.endpoint}/{id}", data.model_dump())

        @classmethod
        def delete(cls, id: int, force: bool = False, cascade: bool = False) -> dict|bool:
            return ReqDB.api.delete(f"{cls.endpoint}/{id}", force, cascade)

        @classmethod
        def add(cls, data: Base) -> dict|bool:
            if not isinstance(data, cls.model):
                raise TypeError(f"Data not the correct model ({cls.model.__name__})")
            r = ReqDB.api.add(f"{cls.endpoint}", data.model_dump())
            return r

    class Tags(Entity):
        endpoint = "tags"
        model = Tag

    class Topics(Entity):
        endpoint = "topics"
        model = Topic

    class Requirements(Entity):
        endpoint = "requirements"
        model = Requirement

    class ExtraTypes(Entity):
        endpoint = "extraTypes"
        model = ExtraType

    class ExtraEntries(Entity):
        endpoint = "extraEntries"
        model = ExtraEntry

    class Catalogues(Entity):
        endpoint = "catalogues"
        model = Catalogue

    class Comment(Entity):
        endpoint = "comments"
        model = Comment

    class Coffee(Entity):
        endpoint = "coffee"
        model = None

    class Audit(Entity):
        endpoint = "audit"
        model = None

        @classmethod
        def _targetCheck(cls, obj: str):
            target = ["extraEntries", "extraTypes", "requirements", "tags", "topics", "catalogues", "comments"]
            if obj not in ["extraEntries", "extraTypes", "requirements", "tags", "topics", "catalogues", "comments"]:
                raise KeyError(f"Audit object can only one of: {', '.join(target)}")

        @classmethod
        def get(cls, obj: str, id: int) -> dict|bool:
            cls._targetCheck(obj)
            return ReqDB.api.get(f"{cls.endpoint}/{obj}/{id}")

        @classmethod
        def all(cls, obj: str) -> dict|bool:
            cls._targetCheck(obj)
            return ReqDB.api.get(f"{cls.endpoint}/{obj}")

        @classmethod
        def update(cls, id, data: Base):
            raise NotImplementedError

        @classmethod
        def delete(cls, id):
            raise NotImplementedError

        @classmethod
        def add(cls, data: Base):
            raise NotImplementedError

    class Configuration(Entity):
        endpoint = "config"
        model = Configuration

        @classmethod
        def delete(cls, id):
            raise NotImplementedError

        @classmethod
        def add(cls, data: Base):
            raise NotImplementedError