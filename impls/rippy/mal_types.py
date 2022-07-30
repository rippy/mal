#!/usr/bin/env python3

from numbers import Number


class MalType(object):
    def __init__(self) -> None:
        x = True

class MalList(MalType):
    def __init__(self, items: list) -> None:
        self.items = items

class MalScalar(MalType):
    def __init__(self) -> None:
        x = True

class MalSymbol(MalScalar):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

class MalNumber(MalScalar):
    def __init__(self, s: str) -> None:
        self.s = s
        self.x = self.s # TODO more of a number
