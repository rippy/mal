#!/usr/bin/env python3

# Add a new file core.qx and define an associative data structure ns (namespace) that maps symbols to functions.
# Move the numeric function definitions into this structure.

# class MalNamespace(object):
#     def __init__(self) -> None:
#         self.functions = {}

from mal_types import *
from printer import pr_str

###############################################################################################
# Numeric functions
def mal_add(p1: MalNumber, p2: MalNumber) -> MalNumber:
    v = p1.x + p2.x
    r = MalNumber(v)
    return r

def mal_sub(p1: MalNumber, p2: MalNumber) -> MalNumber:
    v = p1.x - p2.x
    r = MalNumber(v)
    return r

def mal_mul(p1: MalNumber, p2: MalNumber) -> MalNumber:
    v = p1.x * p2.x
    r = MalNumber(v)
    return r

def mal_div(p1: MalNumber, p2: MalNumber) -> MalNumber:
    v = p1.x / p2.x
    r = MalNumber(v)
    return r


###############################################################################################
# Comparison functions
def mal_equalp(*args) -> MalBoolean:
    """
    equalp: compare the first two parameters and return true if they are the same type and contain the same value.
            In the case of equal length lists, each element of the list should be compared for equality and
            if they are the same return true, otherwise false.
    """
    assert len(args) == 2,                 "expected 2 parameters, received %s parameters" % (len(args))

    r = MalFalse()
    if args[0] == args[1]:  # uses the __eq__ on each of the MalType objects
        r = MalTrue()
    return r

def mal_lessp(*args) -> MalBoolean:
    """
    mal_lessp: treat the first two parameters as numbers and return true if arg0 < arg1, otherwise return false
    """
    assert len(args) == 2,                 "expected 2 parameters, received %s parameters" % (len(args))
    assert isinstance(args[0], MalNumber), "expected arg0 <class 'MalNumber'>, found %s" % (type(args))
    assert isinstance(args[1], MalNumber), "expected arg1 <class 'MalNumber'>, found %s" % (type(args))

    r = MalFalse()
    if args[0] < args[1]:  # uses the __lt__ on each of the MalNumber objects
        r = MalTrue()
    return r

def mal_lessequalp(*args) -> MalBoolean:
    """
    mal_lessequalp: treat the first two parameters as numbers and return true if arg0 <= arg1, otherwise return false
    """
    assert len(args) == 2,                 "expected 2 parameters, received %s parameters" % (len(args))
    assert isinstance(args[0], MalNumber), "expected arg0 <class 'MalNumber'>, found %s" % (type(args))
    assert isinstance(args[1], MalNumber), "expected arg1 <class 'MalNumber'>, found %s" % (type(args))

    r = MalFalse()
    if args[0] <= args[1]:  # uses the __le__ on each of the MalNumber objects
        r = MalTrue()
    return r

def mal_greaterp(*args) -> MalBoolean:
    """
    greaterp: treat the first two parameters as numbers and return true if arg0 > arg1, otherwise return false
    """
    assert len(args) == 2,                 "expected 2 parameters, received %s parameters" % (len(args))
    assert isinstance(args[0], MalNumber), "expected arg0 <class 'MalNumber'>, found %s" % (type(args))
    assert isinstance(args[1], MalNumber), "expected arg1 <class 'MalNumber'>, found %s" % (type(args))

    r = MalFalse()
    if args[0] > args[1]:  # uses the __gt__ on each of the MalNumber objects
        r = MalTrue()
    return r

def mal_greaterequalp(*args) -> MalBoolean:
    """
    mal_greaterequalp: treat the first two parameters as numbers and return true if arg0 >= arg1, otherwise return false
    """
    assert len(args) == 2,                 "expected 2 parameters, received %s parameters" % (len(args))
    assert isinstance(args[0], MalNumber), "expected arg0 <class 'MalNumber'>, found %s" % (type(args))
    assert isinstance(args[1], MalNumber), "expected arg1 <class 'MalNumber'>, found %s" % (type(args))

    r = MalFalse()
    if args[0] >= args[1]:  # uses the __ge__ on each of the MalNumber objects
        r = MalTrue()
    return r

def mal_nilp(*args) -> MalBoolean:
    """
    nilp: return true if
    """
    assert len(args) == 1,                 "expected 1 parameter, received %s parameters" % (len(args))

    if isinstance(args[0], MalNil):
        return MalTrue()
    return MalFalse()


###############################################################################################
# Collection functions
def mal_list(*args) -> MalList:
    """
    list:  take the parameters and return them as a list.
    """
    assert isinstance(args, tuple), "expected <class 'tuple'>, found %s" % (type(args))
    r = MalList(args)
    return r

def mal_listp(*args) -> MalBoolean:
    """
    list?: return true if the first parameter is a list, false otherwise.
    """
    if isinstance(args[0], MalList):
        return MalTrue()
    return MalFalse()

def mal_emptyp(*args) -> MalBoolean:
    """
    empty?: treat the first parameter as a list and return true if the list is empty, and false if it contains any elements.
    """
    assert isinstance(args[0], MalCollection), "expected <class 'MalCollection'>, found %s" % (type(args))

    if len(args[0].items) == 0:
        return MalTrue()
    return MalFalse()

def mal_count(*args) -> MalNumber:
    """
    count: treat the first parameter as a list and return the number of elements that it contains.
    """

    if len(args) <= 0:
        return MalNumber(0)

    if isinstance(args[0], MalNil):
        return MalNumber(0)

    assert isinstance(args[0], MalCollection), "expected <class 'MalCollection'>, found %s" % (type(args[0]))
    return MalNumber(len(args[0].items))


###############################################################################################
# string functions
def mal_prn(*args) -> MalType:
    """
    prn: calls pr_str on each argument with print_readably set to True, joins the results with " ", prints the string to the screen, and then returns nil.
    """
    l = []
    for o in args:
        l.append(pr_str(o, print_readably=True))
    v = " ".join(l)
    print(v)  # TOOD print here?
    return MalNil()

def mal_println(*args) -> MalString:
    """
    println: calls pr_str on each argument with print_readably set to False, joins the results with " ", prints the string to the screen and then returns nil
    """
    l = []
    for o in args:
        l.append(pr_str(o, print_readably=False))
    v = " ".join(l)
    print(v)  # TOOD print here?
    return MalNil()

def mal_prstr(*args) -> MalType:
    """
    pr-str: calls pr_str on each argument with print_readably set to True, joins the results with " ", and returns the new string.
    """
    l = []
    for o in args:
        l.append(pr_str(o, print_readably=True))
    v = " ".join(l)
    return MalString(v)


def mal_str(*args) -> MalString:
    """
    str: calls pr_str on each argument with print_readably set to False, concatenates the results together ("" separator), and returns the new string.
    """
    l = []
    for o in args:
        l.append(pr_str(o, print_readably=False))
    v = "".join(l)
    return MalString(v)

###############################################################################################
# misc functions
def mal_keyword(p1: MalType) -> MalKeyword:
    """
    keyword: takes a string and returns a keyword with the same name (usually just be prepending the special keyword unicode symbol).
             This function should also detect if the argument is already a keyword and just return it.
    """
    if isinstance(p1, MalKeyword):
        return p1

    assert isinstance(p1, MalString), "expected <class 'MalString'>, found %s" % (type(p1))
    return MalKeyword(p1.value)

def mal_keywordp(p1: MalType) -> MalKeyword:
    """
    keyword?: takes a single argument and returns true (mal true value) if the argument is a keyword, otherwise returns false (mal false value).
    """
    if isinstance(p1, MalKeyword):
        return MalTrue()
    return MalFalse()


###############################################################################################
# hook it all up
namespace = {
    "+":         mal_add,
    "-":         mal_sub,
    "*":         mal_mul,
    "/":         mal_div,

    "equal?":    mal_equalp,
    "nil?":      mal_nilp,
    "=":         mal_equalp,
    "<":         mal_lessp,
    "<=":        mal_lessequalp,
    ">":         mal_greaterp,
    ">=":        mal_greaterequalp,

    "list":      mal_list,
    "list?":     mal_listp,
    "empty?":    mal_emptyp,
    "count":     mal_count,

    "pr-str":    mal_prstr,
    "str":       mal_str,
    "prn":       mal_prn,
    "println":   mal_println,

    "keyword":   mal_keyword,
    "keyword?":  mal_keywordp,
}
