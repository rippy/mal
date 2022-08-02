#!/usr/bin/env python3

from numbers import Number
import typing


###############################################################################################
# See also:
#   https://stackoverflow.com/questions/3588776/how-is-eq-handled-in-python-and-in-what-order
#   https://www.geeksforgeeks.org/operator-overloading-in-python/
#   https://stackoverflow.com/questions/2909106/whats-a-correct-and-good-way-to-implement-hash
###############################################################################################

class MalType(object):
    def __init__(self) -> None:
        self.value = None

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        #print('MalType __eq__ called')
        if not isinstance(other, MalType):
            return False
        return self.value == other.value

    def __ne__(self, other):
        #print('MalType __eq__ called')
        return self.value != other.value

    def __hash__(self):
        #hv = hash(self.value)
        hv = hash(str(type(self)) + ":" + self.value)
        return hv

class MalNil(MalType):
    def __init__(self) -> None:
        self.value = None

    def __repr__(self) -> str:
        return """MalNil()"""

    def __eq__(self, other):
        #print('MalNil __eq__ called')
        if not isinstance(other, MalNil):
            return False
        return True

    def __hash__(self):
        hv = hash(str(type(self)) + ":nil")
        return hv


###############################################################################################
# collections
class MalCollection(MalType):
    def __init__(self, items: list) -> None:
        self.items = items
        self.value = items

    def __eq__(self, other):
        #print('MalCollection __eq__ called')
        if not isinstance(other, MalCollection):
            return False

        M, N = len(self.items), len(other.items)
        if (M == 0) and (N == 0):
            return True
        if (M != N):
            return False

        for i in range(0, M):
            a, b = self.items[i], other.items[i]
            if a != b:
                return False
        return True


class MalList(MalCollection):
    def __init__(self, items: list) -> None:
        self.items = items
        self.value = items

    def __repr__(self) -> str:
        l = []
        for e in self.items:
            l.append(repr(e))
        return "MalList([" + ", ".join(l) + "])"

class MalVector(MalCollection):
    def __init__(self, items: list) -> None:
        self.items = items
        self.value = items

    def __repr__(self) -> str:
        l = []
        for e in self.items:
            l.append(repr(e))
        return "[" + " ".join(l) + "]"

class MalHashmap(MalCollection):
    def __init__(self, values: dict) -> None:
        self.values = values
        self.value = values

    def __repr__(self) -> str:
        l = []
        for k, v in self.values:
            l.append(repr(k))
            l.append(repr(v))
        return "{" + " ".join(l) + "}"


###############################################################################################
# Scalars
class MalScalar(MalType):
    def __init__(self) -> None:
        pass

class MalString(MalScalar):
    def __init__(self,  value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return """MalString("%s")""" % self.value

class MalSymbol(MalScalar):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.value = symbol

    def __repr__(self) -> str:
        return """MalSymbol("%s")""" % self.symbol

class MalKeyword(MalScalar):
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return """MalKeyword("%s")""" % self.value

class MalBoolean(MalScalar):
    def __init__(self, value: bool) -> None:
        self.value = value

    def __repr__(self) -> str:
        return """MalTrue()"""


class MalTrue(MalBoolean):
    def __init__(self) -> None:
        self.value = True

    def __repr__(self) -> str:
        return """MalTrue()"""

class MalFalse(MalBoolean):
    def __init__(self) -> None:
        self.value = False

    def __repr__(self) -> str:
        return """MalFalse()"""

class MalNumber(MalScalar):
    """
        ==	__eq__(self, other)
        !=	__ne__(self, other)

        <	__lt__(self, other)
        <=	__le__(self, other)
        >	__gt__(self, other)
        >=	__ge__(self, other)
    """
    def __init__(self, s: str) -> None:
        self.s = s
        self.x = int(self.s)   # TODO more number stuff here
        self.value = self.x

    def __repr__(self) -> str:
        return """MalNumber(%s)""" % self.s

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


###############################################################################################
# Misc

class MalFunction(MalType):
    """
        TBD
    """
    def __init__(self, fn: typing.Callable) -> None:
        self.fn = fn
