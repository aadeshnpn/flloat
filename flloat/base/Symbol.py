# -*- coding: utf-8 -*-
from flloat.base.hashable import Hashable
import re
import numpy as np


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
        self.origin = None
        try:
            self._parse()
        except AttributeError:
            # return Symbol(self.name)
            pass

    def _parse(self):
        # Normal syntax
        # P_[a,b,c,d][3, none, <=]
        # New notation with three agruments and multiple indexing
        temp = re.match('^P_\[[A-Za-z0-9,\]]+', self.name)
        if temp is None:
            temp = re.match('[A-Za-z0-9_]*', self.name)
            fname = temp.group()
            fnames = fname.split('_')
            self.fname = fnames[0]
            self.keys = '_'.join(fnames[1:])
            args = re.search('\[[a-zA-Z0-9,\-_<>=!]*\]', self.name)
            args = args.group()
            arg1, arg2 = args.split(',')
            self.state = arg1[1:]
            self.operator = arg2[:-1]
            self.norm = 'none'
        else:
            fname = temp.group()
            fnames = fname.split('_')
            # Get the function name
            self.fname = fnames[0]
            # Get the keys
            temp = re.search('[A-Za-z0-9,]+', fnames[1])
            temp = temp.group()
            self.keys = temp.split(',')
            # self.key = self.keys[0]
            args = re.search('[[A-Za-z0-9,.\-|!=<>]+]$', self.name)
            args = args.group()
            args = re.search('[A-Za-z0-9,.\-|!=<>]+', args)
            args = args.group()
            try:
                self.state, self.norm, self.operator,self.origin = args.split(',')
            except ValueError:
                self.state, self.norm, self.operator = args.split(',')
            if self.norm == '|.|2':
                self.norm = 2
            elif self.norm == '|.|1':
                self.norm = 1
            elif self.norm == '|.|inf':
                self.norm = np.inf
            elif self.norm == '|.|city':
                self.norm = 'cityblock'
            elif self.norm == 'none':
                self.norm = 'none'
            else:
                self.norm = 2

    def __repr__(self):
        return self.name
