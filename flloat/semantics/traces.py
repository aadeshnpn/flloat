from abc import abstractmethod
from typing import List, Set

from flloat.base.symbols import Symbol
from flloat.base.truths import Truth
from flloat.helpers import Hashable
from flloat.semantics.pl import PLInterpretation


class FiniteTrace(Hashable):
    def __init__(self, trace: List[PLInterpretation]):
        super().__init__()
        self.trace = trace

    def _members(self):
        return tuple(self.trace)

    @staticmethod
    def from_symbol_sets(l: List[Set[Symbol]]):
        return FiniteTrace([PLInterpretation(frozenset(s)) for s in l])

    def length(self):
        return len(self.trace)

    def last(self):
        return len(self.trace)-1

    def _position_is_legal(self, position: int):
        return position>=0 and position <= self.last()

    def get(self, position: int) -> PLInterpretation:
        assert self._position_is_legal(position)
        return self.trace[position]

    def segment(self, start: int, end: int):
        if not self._position_is_legal(start) or not self._position_is_legal(end):
            raise ValueError("Start or end position are not valid")
        return FiniteTrace(self.trace[start: end])

    def __str__(self):
        return "Trace (length=%s)" % self.length() + "\n\t" + \
               "\n\t".join("%d: {" % i + ", ".join(map(str, sorted(e))) + "}" for i, e in enumerate(self.trace))


class FiniteTraceTruth(Truth):
    @abstractmethod
    def truth(self, i: FiniteTrace, pos: int):
        raise NotImplementedError
