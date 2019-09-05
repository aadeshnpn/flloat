# -*- coding: utf-8 -*-
from flloat.base.hashable import Hashable
import re


class Symbol(str, Hashable):
    def __init__(self, name):
        str.__init__(self)
        Hashable.__init__(self)
        self.name = name

    def _members(self):
        return self.name


class FunctionSymbol(Symbol):
    def __init__(self, name):
        """Functional Symbol."""
        super().__init__(name)
        self.name = name
        try:
            self._parse()
        except AttributeError:
            # return Symbol(self.name)
            pass

    def _parse(self):
        temp = re.match('[A-Za-z0-9]*', self.name)
        self.fname = temp.group()
        args = re.search('\[[a-zA-Z0-9,_<>=!]*\]', self.name)
        args = args.group()
        arg1, arg2 = args.split(',')
        self.state = arg1[1:]
        self.operator = arg2[:-1]

    def __repr__(self):
        return self.name

