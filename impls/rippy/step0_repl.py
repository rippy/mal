#!/usr/bin/env python3

import atexit
import os
import readline as rl

###############################################################################################
# See also:
# - https://github.com/kanaka/mal/blob/master/process/guide.md#step0
# - https://docs.python.org/3/library/readline.html
# --  https://eli.thegreenplace.net/2016/basics-of-using-the-readline-library
# - https://docs.python.org/3/library/typing.html
#
# Add the 4 trivial functions READ, EVAL, PRINT, and rep (read-eval-print).
# READ, EVAL, and PRINT are basically just stubs that return their first parameter
# (a string if your target language is a statically typed) and rep calls them in
# order passing the return to the input of the next.
#
# Add a main loop that repeatedly prints a prompt (needs to be "user> " for later
# tests to pass), gets a line of input from the user, calls rep with that line of
# input, and then prints out the result from rep. It should also exit when you send it an EOF (often Ctrl-D).
###############################################################################################

def READ(p1: str) -> str:
    return p1

def EVAL(p1: str) -> str:
    return p1

def PRINT(p1: str) -> str:
    return p1

def rep(p1: str) -> str:
    return PRINT(EVAL(READ(p1)))

if __name__ == '__main__':

    try:
        histfile = os.path.join(os.path.expanduser("~"), ".mal_history")
        rl.read_history_file(histfile)
        rl.set_history_length(100) # -1  mean infinite
        atexit.register(rl.write_history_file, histfile)
    except FileNotFoundError:
        pass

    ps1 = "user> "

    try:
        while True:
            s = input(ps1).strip()
            r = rep(s)
            #print('[{0}]'.format(r))
            print(r)
    except (EOFError, KeyboardInterrupt) as e:
        print('\nShutting down...')



