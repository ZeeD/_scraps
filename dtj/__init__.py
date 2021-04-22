from dataclasses import dataclass
from datetime import date
from typing import List

from dataclasses_json import DataClassJsonMixin

RAW = '''{
    "foo": "bar",
    "baz": [
        {
            "qux": 1,
            "quux": "2020-01-01"
        },
        {
            "qux": 2,
            "quux": "2020-01-02"
        }
    ],
    "pippo": true
}
'''


@dataclass
class BazElement(DataClassJsonMixin):
    qux: int
    quux: date


@dataclass
class C(DataClassJsonMixin):
    foo: str
    baz: List[BazElement]
    pippo: bool


def main() -> None:
    obj = C.from_json(RAW)
    print(obj)
    raw = obj.to_json()
    print(raw)
