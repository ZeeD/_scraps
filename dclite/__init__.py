from dataclasses import dataclass, is_dataclass, fields
from datetime import datetime
from sqlite3 import connect
from typing import TypeVar, Any, Iterator

T = TypeVar('T')


class dclite:
    def __init__(self, database: str):
        self.con = connect(database)

    def create_table(self, cls: type[T]) -> None:
        assert is_dataclass(cls)
        names = [field.name for field in fields(cls)]

        sql = f'CREATE TABLE {cls.__name__}({", ".join(names)})'
        print(sql)

        self.con.cursor().execute(sql)
        self.con.commit()

    def insert(self, dc: T) -> None:
        assert is_dataclass(dc)
        names = [field.name for field in fields(dc)]

        sql = f'INSERT INTO {dc.__class__.__name__}({", ".join(names)}) values ({", ".join("?" for _ in names)})'
        values = tuple(getattr(dc, name) for name in names)
        print(sql, values)

        self.con.cursor().execute(sql, values)
        self.con.commit()

    def select(self, cls: type[T], **where: Any) -> Iterator[T]:
        assert is_dataclass(cls)
        names = [field.name for field in fields(cls)]
        assert all(k in names for k in where)

        sql = f'SELECT {", ".join(names)} from {cls.__name__} where {" and ".join(f"{k}=?" for k in where)}'
        values = tuple(where.values())
        print(sql, values)

        cur = self.con.cursor()
        cur.execute(sql, values)

        for row in cur.fetchall():
            yield cls(**{n: v for n, v in zip(names, row)})  # type: ignore


def main() -> None:
    @dataclass
    class Foo:
        bar: int
        baz: str
        qux: datetime

    db = dclite(':memory:')
    db.create_table(Foo)
    db.insert(Foo(bar=123, baz='str', qux=datetime(1982, 11, 5)))
    db.update(Foo(bar=123, baz='str', qux=datetime(1982, 11, 5)),
              bar=123)
    for row in db.select(Foo, bar=123):
        print(row)
        assert isinstance(row, Foo)
    db.delete(Foo, bar=123)
    db.drop_table(Foo)


if __name__ == '__main__':
    main()
