from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from dataclasses import is_dataclass
from datetime import date
from datetime import datetime
from decimal import Decimal
from json import dumps as dumps_
from json import loads as loads_
from typing import Type
from typing import TypeVar
from typing import cast


def dumps(obj: object) -> str:
    def m(obj: object) -> object:
        if is_dataclass(obj):
            return m(asdict(obj))
        if isinstance(obj, dict):
            return {str(k): m(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [m(v) for v in obj]
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return obj
    return dumps_(m(obj))


T = TypeVar('T')


def loads(cls: Type[T], raw: str) -> T:
    def m(cls: Type[T], mapped: object) -> T:
        if is_dataclass(cls):
            return cls(**{f.name: m(f.type, cast(dict[str, object], mapped)[f.name])  # type: ignore
                          for f in fields(cls)})
        if issubclass(cls, dict):
            return cast(T, {k: m(cast(Type[T], object), v)  # TODO: retrieve dict[,...] value @ runtime
                            for k, v in (cast(dict[str, object], mapped)).items()})
        if issubclass(cls, (list, tuple)):
            return cast(T, cls(m(cast(Type[T], object), e)  # TODO: retrieve list[...] value @ runtime
                               for e in mapped))
        if issubclass(cls, (date, datetime)):
            return cast(T, cls.fromisoformat(cast(str, mapped)))
        return cast(T, mapped)

    return m(cls, loads_(raw))


def main() -> None:
    @dataclass
    class Child:
        a: int
        b: datetime

    @dataclass
    class Pojo:
        foo: str
        bar: list[float]
        baz: bool
        child: Child

    OBJ = Pojo('ciao', [.1, .2, .3], True, Child(1, datetime.fromordinal(1)))
    JSON = '{"foo": "ciao", "bar": [0.1, 0.2, 0.3], "baz": true, "child": {"a": 1, "b": "0001-01-01T00:00:00"}}'

    assert JSON == dumps(OBJ), dumps(OBJ)
    assert OBJ == loads(Pojo, JSON), loads(Pojo, JSON)
