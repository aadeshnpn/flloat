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
