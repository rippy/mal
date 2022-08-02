#!/usr/bin/env python3

from mal_types import *

def _escape(p1: MalString) -> str:
    s = p1.value
    s = s.replace('\\', '\\\\')
    s = s.replace( '"',  '\\"')
    s = s.replace('\n',  '\\n')
    return s


def pr_str(o: MalType, print_readably:bool=False) -> str:
    if o is None:
        raise Exception("unknown type: None")

    if isinstance(o, MalNil):
        return "nil"

    if isinstance(o, MalString):
        """
        When print_readably is true, doublequotes, newlines, and backslashes are translated into their printed representations (the reverse of the reader).
        The PRINT function in the main program should call pr_str with print_readably set to true.
        """
        if print_readably:
            return '"' + _escape(o) + '"'
        else:
            return o.value

    if isinstance(o, MalBoolean):
        return str(o.value).lower()

    if isinstance(o, MalSymbol):
        return o.symbol

    if isinstance(o, MalKeyword):
        return ":" + o.value

    if isinstance(o, MalNumber):
        return str(o.x)

    if isinstance(o, MalList):
        l = []
        for e in o.items:
            l.append(pr_str(e))
        return "(" + " ".join(l) + ")"

    if isinstance(o, MalVector):
        l = []
        for e in o.items:
            l.append(pr_str(e))
        return "[" + " ".join(l) + "]"

    if isinstance(o, MalHashmap):
        l = []
        for k, v in o.values.items():
            l.append(pr_str(k))
            l.append(pr_str(v))
        return "{" + " ".join(l) + "}"

    #raise Exception("unknown type: " + type(o))
    #return repr(o)
    return "#" + str(o)