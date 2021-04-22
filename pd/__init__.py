from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import date
from typing import Any
from typing import List

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
    ...
