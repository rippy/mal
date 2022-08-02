#!/usr/bin/env python3

import atexit
import os
import readline as rl
import signal
import traceback


import mal_core
from mal_env import *
from mal_types import *
import reader
import printer


###############################################################################################
# See also:
# - https://github.com/kanaka/mal/blob/master/process/guide.md#step-4-if-fn-do
#
# In this step you will add 3 new special forms (if, fn* and do) and add several more core
# functions to the default REPL environment.
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
                #repl_env.set(a1.symbol, v)
                repl_env.set(a1, v)
                return v

            elif a0.symbol == "let*":
                # create a new environment using the current environment as the outer value and then use the
                # first parameter as a list of new bindings in the "let*" environment.
                new_env = MalEnv(repl_env)
                a1 = ast.items[1]
                bindings = a1

                assert isinstance(bindings, MalCollection), "expected <class 'MalCollection'>, found %s" % (type(bindings))
                assert len(bindings.items) % 2 == 0,        "invalid length"   # validate an even number of items

                # Take the second element of the binding list, call EVAL using the new "let*" environment as
                # the evaluation environment, then call set on the "let*" environment using the first binding
                # list element as the key and the evaluated second element as the value.
                # This is repeated for each odd/even pair in the binding list.
                # Note in particular, the bindings earlier in the list can be referred to by later bindings.
                l = bindings.items
                for i in range(0, len(l)-1, 2):
                    b0, b1 = l[i], l[i+1]
                    v = EVAL(b1, new_env)
                    #new_env.set(b0.symbol, v)
                    new_env.set(b0, v)

                # Finally, the second parameter (third element) of the original let* form is evaluated using the
                # new "let*" environment and the result is returned as the result of the let*
                # (the new let environment is discarded upon completion).
                a2 = ast.items[2]
                #r = eval_ast(a2, new_env)
                r = EVAL(a2, new_env)
                return r

            elif a0.symbol == "do":
                # do: Evaluate all the elements of the list using eval_ast and return the final evaluated element.
                assert isinstance(ast, MalList), "expected <class 'MalList'>, found %s" % (type(ast))

                v = None
                l = ast.items[1:]
                for i in range(0, len(l)):
                    e = l[i]
                    #v = eval_ast(e, repl_env)
                    v = EVAL(e, repl_env)
                return v

            elif a0.symbol == "if":
                # if: Evaluate the first parameter (second element).
                # If the result (condition) is anything other than nil or false, then
                #   evaluate the second parameter (third element of the list) and return the result.
                # Otherwise, evaluate the third parameter (fourth element) and return the result.
                # If condition is false and there is no third parameter, then just return nil.

                a1 = ast.items[1]
                #cond = eval_ast(a1, repl_env)
                cond = EVAL(a1, repl_env)
                if not isinstance(cond, MalFalse) and not isinstance(cond, MalNil):
                    a2 = ast.items[2]
                    #v = eval_ast(a2, repl_env)
                    v = EVAL(a2, repl_env)
                    return v

                if len(ast.items) > 3:
                    assert len(ast.items) == 4,        "invalid length"   # validate an even number of items

                    a3 = ast.items[3]
                    v = MalNil()
                    #v = eval_ast(a3, repl_env)
                    v = EVAL(a3, repl_env)
                    return v

                v = MalNil()
                return v

            elif a0.symbol == "fn*":
                # fn*:  returns a new function closure. The body of that closure does the following:
                #
                #  Create a new environment using env (closed over from outer scope) as the outer parameter,
                #    the first parameter (second list element of ast from the outer scope) as the binds parameter,
                #    and the parameters to the closure as the exprs parameter.
                #
                #  Call EVAL on the second parameter (third list element of ast from outer scope), using the new environment.
                #    Use the result as the return value of the closure.

                def function_closure(*args):
                    a1, a2 = ast.items[1], ast.items[2]
                    bindings = a1
                    new_env = MalEnv(repl_env, bindings.items, args)

                    v = EVAL(a2, new_env)
                    return v

                #r = MalFunction(function_closure)
                r = function_closure
                return r

        el = eval_ast(ast, repl_env)

        f = el.items[0]
        args = el.items[1:]
        r = f(*args)
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
        #symbol = ast.symbol
        # if symbol in repl_env:
        #     return repl_env[symbol]
        # raise Exception("symbol not found")
        symbol = ast
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

def PRINT(s: MalType) -> str:
    result = printer.pr_str(s, print_readably=True)
    return result

def rep(s: str, repl_env: dict) -> str:
    r = READ(s)
    e = EVAL(r, repl_env)
    p = PRINT(e)
    return p

histfile = os.path.join(os.path.expanduser("~"), ".mal_history")
def handler(signum, frame):
    """
    See also https://docs.python.org/3/library/signal.html
    """
    rl.write_history_file(histfile)
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT,  handler)

    try:
        rl.read_history_file(histfile)
        rl.set_history_length(100) # -1  mean infinite
        atexit.register(rl.write_history_file, histfile)
    except FileNotFoundError:
        pass

    try:
        repl_env = MalEnv(None)
        for symbol, fn in mal_core.namespace.items():
            #repl_env.set(symbol, fn)
            repl_env.set(MalSymbol(symbol), fn)

        # pre-defined functions written in mal itself
        rep("""
           (def! not (fn* (a)
                       (if a false true)))
        """, repl_env)

        ps1 = "user> "
        while True:
            try:
                s = input(ps1).strip()
                r = rep(s, repl_env)
                print(r)
            except AssertionError as ae:
                print("Assertion error: " + str(ae))
                traceback.print_exception(type(ae), ae, ae.__traceback__)
            except EOFError as ex:
                # user hit ^D, just loop around
                print()
            except Exception as ex:
                #print(str(ex))
                traceback.print_exception(type(ex), ex, ex.__traceback__)
    except (EOFError, KeyboardInterrupt) as e:
        print('\n')  # shutting down...
