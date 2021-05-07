from dataclasses import dataclass
from dataclasses import fields
from dataclasses import is_dataclass
from datetime import datetime
from sqlite3 import connect
from sqlite3.dbapi2 import Connection
from typing import Any, Generic, Protocol, Optional
from typing import Iterator
from typing import TypeVar
from sys import stderr


T = TypeVar('T')


class _Where(Generic[T]):
    def __init__(self, con: Connection, dc: T):
        self.con = con
        self.dc = dc

    def where(self, **kwargs: Any) -> None:
        assert is_dataclass(self.dc)
        names = [field.name for field in fields(self.dc)]
        assert all(k in names for k in kwargs)

        sql = f'UPDATE {self.dc.__class__.__name__} SET {", ".join(f"{name}=?" for name in names)} WHERE {" and ".join(f"{k}=?" for k in kwargs)}'
        values = tuple(getattr(self.dc, name)
                       for name in names) + tuple(kwargs.values())
        print(sql, values, file=stderr)

        cur = self.con.cursor()
        cur.execute(sql, values)
        self.con.commit()


class dclite:
    def __init__(self, database: str):
        self.con = connect(database)

    def create_table(self, cls: type[T]) -> None:
        assert is_dataclass(cls)
        names = [field.name for field in fields(cls)]

        sql = f'CREATE TABLE {cls.__name__}({", ".join(names)})'
        print(sql, file=stderr)

        self.con.cursor().execute(sql)
        self.con.commit()

    def insert(self, dc: T) -> None:
        assert is_dataclass(dc)
        names = [field.name for field in fields(dc)]

        sql = f'INSERT INTO {dc.__class__.__name__}({", ".join(names)}) VALUES ({", ".join("?" for _ in names)})'
        values = tuple(getattr(dc, name) for name in names)
        print(sql, values, file=stderr)

        self.con.cursor().execute(sql, values)
        self.con.commit()

    def select(self, cls: type[T], **where: Any) -> Iterator[T]:
        assert is_dataclass(cls)
        names = [field.name for field in fields(cls)]
        assert all(k in names for k in where)

        sql = f'SELECT {", ".join(names)} FROM {cls.__name__} WHERE {" and ".join(f"{k}=?" for k in where)}'
        values = tuple(where.values())
        print(sql, values, file=stderr)

        cur = self.con.cursor()
        cur.execute(sql, values)

        for row in cur.fetchall():
            yield cls(**{n: v for n, v in zip(names, row)})  # type: ignore

    def set(self, dc: T) -> _Where[T]:
        return _Where(self.con, dc)

    def delete(self, cls: type[T], **where: Any) -> None:
        assert is_dataclass(cls)
        names = [field.name for field in fields(cls)]
        assert all(k in names for k in where)

        sql = f'DELETE FROM {cls.__name__} where {" and ".join(f"{k}=?" for k in where)}'
        values = tuple(where.values())
        print(sql, values, file=stderr)

        cur = self.con.cursor()
        cur.execute(sql, values)
        self.con.commit()

    def drop_table(self, cls: type[T]) -> None:
        assert is_dataclass(cls)

        sql = f'DROP TABLE {cls.__name__}'
        print(sql, file=stderr)

        self.con.cursor().execute(sql)
        self.con.commit()


def main() -> None:
    @dataclass
    class Foo:
        bar: int
        baz: str
        qux: datetime

    db = dclite(':memory:')
    db.create_table(Foo)
    db.insert(Foo(bar=123, baz='str', qux=datetime(1982, 11, 5)))
    db.set(Foo(bar=456, baz='str', qux=datetime(1982, 11, 5))).where(bar=123)
    for row in db.select(Foo, bar=456):
        print(row)
        assert isinstance(row, Foo)
    db.delete(Foo, bar=123)
    db.drop_table(Foo)


if __name__ == '__main__':
    main()
