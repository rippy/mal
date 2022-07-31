#!/usr/bin/env python3

from numbers import Number


class MalType(object):
    def __init__(self) -> None:
        x = True

    def __repr__(self) -> str:
        return str(self)

###############################################################################################
# collections
class MalCollection(MalType):
    def __init__(self) -> None:
        pass

class MalList(MalCollection):
    def __init__(self, items: list) -> None:
        self.items = items

    def __repr__(self) -> str:
        l = []
        for e in self.items:
            l.append(repr(e))
        return "(" + " ".join(l) + ")"

class MalVector(MalCollection):
    def __init__(self, items: list) -> None:
        self.items = items

    def __repr__(self) -> str:
        l = []
        for e in self.items:
            l.append(repr(e))
        return "[" + " ".join(l) + "]"

class MalHashmap(MalCollection):
    def __init__(self, dict: hash) -> None:
        self.dict = dict

    # def set(self, k, v):
    #     self.dict[k] = v

    # def get(self, k):
    #     return self.dict[k]

    def __repr__(self) -> str:
        l = []
        for k, v in self.dict:
            l.append(repr(k))
            l.append(repr(v))
        return "{" + " ".join(l) + "}"


###############################################################################################
# scalars
class MalScalar(MalType):
    def __init__(self) -> None:
        x = True

class MalSymbol(MalScalar):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def __repr__(self) -> str:
        return "MalSymbol(%s)" % self.symbol

class MalNumber(MalScalar):
    def __init__(self, s: str) -> None:
        self.s = s
        self.x = int(self.s) # TODO more of a number

    def __repr__(self) -> str:
        return "MalNumber(%s)" % self.s

