#!/usr/bin/env python3

import atexit
import os
import readline as rl
from mal_types import *

import reader
import printer

###############################################################################################
# See also:
# - https://github.com/kanaka/mal/blob/master/process/guide.md#step-1-read-and-print
#
# In this step, your interpreter will "read" the string from the user and parse it into an internal
# tree data structure (an abstract syntax tree) and then take that data structure and "print" it
# back to a string.
###############################################################################################

def READ(s: str) -> str:
    result = reader.read_str(s)
    return result

def EVAL(o: MalType) -> MalType:
    result = o
    return result

def PRINT(s: str) -> str:
    result = printer.pr_str(s)
    return result

def rep(s: str) -> str:
    result = PRINT(EVAL(READ(s)))
    return result

if __name__ == '__main__':
    try:
        histfile = os.path.join(os.path.expanduser("~"), ".mal_history")
        rl.read_history_file(histfile)
        rl.set_history_length(100) # -1  mean infinite
        atexit.register(rl.write_history_file, histfile)
    except FileNotFoundError:
        pass

    try:
        ps1 = "user> "
        while True:
            try:
                s = input(ps1).strip()
                r = rep(s)
                print(r)
            except (Exception) as e:
                print(str(e))
    except (EOFError, KeyboardInterrupt) as e:
        print('\nShutting down...')