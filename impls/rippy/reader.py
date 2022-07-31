#!/usr/bin/env python3

import re
from mal_types import *

class Reader(object):
    def __init__(self, tokens) -> None:
        self.position = 0
        self.tokens = tokens

    def next(self) -> str:
        r = self.tokens[self.position]
        self.position += 1
        return r

    def peek(self) -> str:
        r = self.tokens[self.position]
        return r

    def has_more(self) -> bool:
        r = self.position < len(self.tokens)
        return r


def tokenize(s: str) -> list:
    tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    return [t for t in re.findall(tre, s) if t[0] != ';']


def read_str(s: str) -> MalType:
    tokens = tokenize(s)
    if len(tokens) == 0: raise Exception("blank line")
    reader = Reader(tokens)
    result = read_form(reader)
    return result

def read_form(reader: Reader) -> MalType:
    token = reader.peek()
    if token[0] == ';':
        reader.next()
        return None
    elif "(" == token:
        reader.next()
        result = read_list(reader)
    elif "[" == token:
        reader.next()
        result = read_vector(reader)
    elif "{" == token:
        reader.next()
        result = read_hashmap(reader)
    else:
        result = read_atom(reader)
    return result

def read_list(reader: Reader) -> MalList:
    r = []
    while True:
        if not(reader.has_more()):
            raise Exception("end of input")
        token = reader.peek()
        if token == ")":
            reader.next() # skip over the )
            break
        v = read_form(reader)
        r.append(v)
    return MalList(r)

def read_vector(reader: Reader) -> MalVector:
    r = []
    while True:
        if not(reader.has_more()):
            raise Exception("end of input")
        token = reader.peek()
        if token == "]":
            # skip over the ]
            break
        v = read_form(reader)
        r.append(v)
    return MalVector(r)

def read_hashmap(reader: Reader) -> MalList:
    r = {}
    while True:
        if not(reader.has_more()):
            raise Exception("end of input")
        token = reader.peek()
        if token == "}":
            reader.next() # skip over the }
            break
        k = read_form(reader)
        v = read_form(reader)
        r[k] = v
    return MalHashmap(r)

# https://stackoverflow.com/questions/40097590/detect-whether-a-python-string-is-a-number-or-a-letter
def is_number(n) -> bool:
    is_number = True
    try:
        num = float(n)
        is_number = (num == num)
    except ValueError:
        is_number = False
    except TypeError:
        is_number = False
    return is_number

def read_atom(reader: Reader) -> MalType:
    token = reader.next()

    result = None
    if is_number(token):
        result = MalNumber(token)
    else:
        result = MalSymbol(token)
    return result


