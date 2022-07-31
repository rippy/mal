#!/usr/bin/env python3

import atexit
import os
import readline as rl

from mal_env import *
from mal_types import *
import reader
import printer

###############################################################################################
# See also:
# - https://github.com/kanaka/mal/blob/master/process/guide.md#step-2-eval
#
# In step 1 your mal interpreter was basically just a way to validate input and eliminate
# extraneous white space. In this step you will turn your interpreter into a simple number
# calculator by adding functionality to the evaluator (EVAL).
###############################################################################################

def READ(s: str) -> str:
    result = reader.read_str(s)
    return result

def EVAL(ast: MalType, repl_env: MalEnv) -> MalType:
    """
    Modify EVAL to check if the first parameter ast is a list.

    - ast is not a list: then return the result of calling eval_ast on it.
    - ast is a empty list: return ast unchanged.
    - ast is a list: call eval_ast to get a new evaluated list.
    --- Take the first item of the evaluated list and call it as function using the rest of the evaluated list as its arguments.
    """
    if not isinstance(ast, MalType):
        raise Exception("unknown error")

    if isinstance(ast, MalList):
        if len(ast.items) == 0:
            return ast

        a0 = ast.items[0]
        if isinstance(a0, MalSymbol):
            if a0.symbol == "def!":
                # call the set method of the current environment (second parameter of EVAL called env) using the
                # unevaluated first parameter (second list element) as the symbol key
                # and the evaluated second parameter as the value.
                a1, a2 = ast.items[1], ast.items[2]
                #v = eval_ast(a2, repl_env)
                v = EVAL(a2, repl_env)
                repl_env.set(a1.symbol, v)
                return v

            elif a0.symbol == "let*":
                # create a new environment using the current environment as the outer value and then use the
                # first parameter as a list of new bindings in the "let*" environment.
                new_env = MalEnv(repl_env)
                a1 = ast.items[1]
                bindings = a1

                assert(isinstance(bindings, MalCollection))  # validate we have a MalCollection
                assert(len(bindings.items) % 2 == 0)         # validate an even number of items

                # Take the second element of the binding list, call EVAL using the new "let*" environment as
                # the evaluation environment, then call set on the "let*" environment using the first binding
                # list element as the key and the evaluated second element as the value.
                # This is repeated for each odd/even pair in the binding list.
                # Note in particular, the bindings earlier in the list can be referred to by later bindings.
                l = bindings.items
                for i in range(0, len(l)-1, 2):
                    b0, b1 = l[i], l[i+1]
                    v = EVAL(b1, new_env)
                    new_env.set(b0.symbol, v)

                # Finally, the second parameter (third element) of the original let* form is evaluated using the
                # new "let*" environment and the result is returned as the result of the let*
                # (the new let environment is discarded upon completion).
                a2 = ast.items[2]
                #r = eval_ast(a2, new_env)
                r = EVAL(a2, new_env)
                return r

        el = eval_ast(ast, repl_env)

        f = el.items[0]
        r = f(*el.items[1:])
        return r

    if isinstance(ast, MalVector):
        if len(ast.items) == 0:
            return ast
        el = eval_ast(ast, repl_env)
        return el

    if isinstance(ast, MalHashmap):
        if len(ast.values) == 0:
            return ast
        el = eval_ast(ast, repl_env)
        return el

    return eval_ast(ast, repl_env)


#def eval_ast(ast: MalType, repl_env: dict) -> str:
def eval_ast(ast: MalType, repl_env: MalEnv):
    """
    eval_ast switches on the type of ast as follows:
    -    symbol:  lookup the symbol in the environment structure and return the value or raise an error if no value is found
    -      list:  return a new list   that is the result of calling EVAL on each of the members of the list
    -    vector:  return a new vector that is the result of calling EVAL on each of the members of the vector.
    -  hash-map:  return a new hash-map which consists of key-value pairs where
    --               the key is a key from the hash-map and the value is the result of calling EVAL on the corresponding value.
    --               (depending on the implementation of maps, it may be convenient to also call EVAL on keys.
    --                The result is the same because keys are not affected by evaluation)
    - otherwise:  return the original ast value
    """
    if isinstance(ast, MalSymbol):
        symbol = ast.symbol
        # if symbol in repl_env:
        #     return repl_env[symbol]
        # raise Exception("symbol not found")
        return repl_env.find(symbol)

    if isinstance(ast, MalList):
        l = []
        for o in ast.items:
            v = EVAL(o, repl_env)
            l.append(v)
        r = MalList(l)
        return r

    if isinstance(ast, MalVector):
        l = []
        for o in ast.items:
            v = EVAL(o, repl_env)
            l.append(v)
        r = MalVector(l)
        return r

    if isinstance(ast, MalHashmap):
        d = {}
        for k, v in ast.values.items():
            d[k] = EVAL(v, repl_env)
        r = MalHashmap(d)
        return r

    return ast

def PRINT(s: str) -> str:
    result = printer.pr_str(s)
    return result

def rep(s: str, repl_env: dict) -> str:
    r = READ(s)
    e = EVAL(r, repl_env)
    p = PRINT(e)
    return p

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

if __name__ == '__main__':
    try:
        histfile = os.path.join(os.path.expanduser("~"), ".mal_history")
        rl.read_history_file(histfile)
        rl.set_history_length(100) # -1  mean infinite
        atexit.register(rl.write_history_file, histfile)
    except FileNotFoundError:
        pass

    try:
        repl_env = MalEnv(None)
        # repl_env.set(MalSymbol("+"), mal_add)
        # repl_env.set(MalSymbol("-"), mal_sub)
        # repl_env.set(MalSymbol("*"), mal_mul)
        # repl_env.set(MalSymbol("/"), mal_div)
        repl_env.set("+", mal_add)
        repl_env.set("-", mal_sub)
        repl_env.set("*", mal_mul)
        repl_env.set("/", mal_div)

        ps1 = "user> "
        while True:
            try:
                s = input(ps1).strip()
                r = rep(s, repl_env)
                print(r)
            except (Exception) as e:
                print(str(e))
    except (EOFError, KeyboardInterrupt) as e:
        print('\nShutting down...')