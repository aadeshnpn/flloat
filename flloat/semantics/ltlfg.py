from typing import FrozenSet, Set, List

from flloat.base.Interpretation import Interpretation
from flloat.base.Symbol import Symbol, FunctionSymbol
from flloat.utils import ObjFactory, ObjConstructor


class _PLGInterpretation(Interpretation):

    def __init__(self, true_propositions: FrozenSet[FunctionSymbol]):
        super().__init__()
        self.true_propositions = frozenset(true_propositions)

    def _members(self):
        # return tuple(sorted(self.true_propositions, key=lambda x: x.name))
        return self.true_propositions

    def __contains__(self, item: FunctionSymbol):
        try:
            print('Inter', item.state, item.operator, self.true_propositions)
            return eval(
                item.state + ' ' + item.operator +
                ' ' + self.true_propositions)
        except AttributeError:
            return item in self.true_propositions
        # return item in self.true_propositions

    def __iter__(self):
        return self.true_propositions.__iter__()

    def __str__(self):
        return "{" + ", ".join(map(str, self._members())) + "}"

    def __repr__(self):
        return self.__str__()


class PLGTrueInterpretation(_PLGInterpretation):
    def __init__(self):
        super().__init__(frozenset())

    def _members(self):
        return PLGTrueInterpretation

    def __contains__(self, item):
        return True


class PLGFalseInterpretation(_PLGInterpretation):
    def __init__(self):
        super().__init__(frozenset())

    def __contains__(self, item):
        return False


class _PLGInterpretationConstructor(ObjConstructor):
    def __call__(self, true_propositions: Set[FunctionSymbol]):
        f_sym = frozenset(true_propositions)
        return super().__call__(f_sym)

    def fromStrings(self, strings: List[str]):
        return self(set(FunctionSymbol(s) for s in strings))


plginterpretation_factory = ObjFactory(_PLGInterpretation)
PLGInterpretation = _PLGInterpretationConstructor(plginterpretation_factory)


class FiniteTrace(Interpretation):
    def __init__(self, trace: List[PLGInterpretation]):
        super().__init__()
        self.trace = trace

    def _members(self):
        return tuple(self.trace)

    @staticmethod
    def fromSymbolSets(l: List[Set[Symbol]]):
        return FiniteTrace([PLGInterpretation(s) for s in l])

    @staticmethod
    def fromStringSets(l: List[Set[str]]):
        return FiniteTrace(
            [PLGInterpretation(frozenset(
                {Symbol(string) for string in s})) for s in l])

    def length(self):
        return len(self.trace)

    def last(self):
        return len(self.trace)-1

    def _position_is_legal(self, position: int):
        return position >= 0 and position <= self.last()

    def get(self, position: int) -> PLGInterpretation:
        assert self._position_is_legal(position)
        return self.trace[position]

    def segment(self, start: int, end: int):
        if not self._position_is_legal(
                start) or not self._position_is_legal(end):
            raise ValueError("Start or end position are not valid")
        return FiniteTrace(self.trace[start: end])

    def __str__(self):
        return "Trace (length=%s)" % self.length() + "\n\t" + \
               "\n\t".join("%d: {"%i + ", ".join(map(str, sorted(e))) + "}" for i, e in enumerate(self.trace))


