#!/usr/bin/env python3

from mal_types import *

def pr_str(o: MalType) -> str:
    if o is None:
        raise Exception("unknown type: None")

    if isinstance(o, MalSymbol):
        return o.symbol

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
    return str(o)