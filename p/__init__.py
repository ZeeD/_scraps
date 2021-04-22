from typing import Protocol


class P(Protocol):
    def __call__(self, foo: int, bar: str) -> bool:
        ...


def impl1(foo: int, bar: str) -> bool:
    return foo < len(bar)


def impl2(foo: int, bar: str) -> bool:
    return foo == len(bar)


def impl3(foo: int, bar: str) -> bool:
    return foo > len(bar)


def wants_cb(cb: P) -> bool:
    return cb(5, 'dieci')


print(impl1.__name__, wants_cb(impl1))
print(impl2.__name__, wants_cb(impl2))
print(impl3.__name__, wants_cb(impl3))
