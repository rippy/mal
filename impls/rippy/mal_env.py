#!/usr/bin/env python3

from mal_types import *

class MalEnv:
    def __init__(self, outer=None, binds=None, exprs=None) -> None:
        """
        Define an Env object that is instantiated with a single outer parameter and starts with an empty
        associative data structure property data.

        Define three methods for the Env object:

         get: takes a symbol key and uses the find method to locate the environment with the key, then returns the matching value.
              (If no key is found up the outer chain, then throws/raises a "not found" error.)
         set: takes a symbol key and a mal value and adds to the data structure
        find: takes a symbol key and if the current environment contains that key then return the environment.
              (If no key is found and outer is not nil then call find (recurse) on the outer environment.)
        """
        self.outer = outer
        self.binds = binds
        self.exprs = exprs

        self.data = {}
        if binds:
            for i in range(len(binds)):
                #if binds[i] == "&":
                if binds[i].value == "&":  # TODO assert binds[i] is a MalSymbol?
                    # Implement Clojure-style variadic function parameters.
                    # If a "&" symbol is encountered in the binds list, the next symbol in the binds list after the "&"
                    # is bound to the rest of the exprs list that has not been bound yet.
                    self.data[binds[i+1]] = exprs[i:]
                    break
                else:
                    assert i < len(exprs), "invalid exprs length, missing value for bind"
                    self.data[binds[i]] = exprs[i]


    def get(self, key: MalSymbol) -> MalType:
        return self.find(key)

    def set(self, key: MalSymbol, value: MalType):
        self.data[key] = value

    def find(self, key: MalSymbol) -> MalType:
        if key in self.data:
            return self.data[key]

        if self.outer is not None:
            return self.outer.find(key)
        raise Exception("env symbol '" + key.value + "' not found")
