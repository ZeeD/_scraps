from dataclasses import dataclass
from dataclasses import field
from datetime import date
from typing import Any
from typing import List

from marshmallow_dataclass import class_schema

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
class BazElement:
    qux: int
    quux: date


@dataclass
class C:
    foo: str
    baz: List[BazElement]
    pippo: bool


def main() -> None:
    c_schema = class_schema(C)()

    obj: C = c_schema.loads(RAW)
    print(obj)
    raw = c_schema.dumps(obj)
    print(raw)
