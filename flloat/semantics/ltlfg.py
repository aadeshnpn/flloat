from abc import abstractmethod
from typing import FrozenSet, Set, List

from flloat.base.Interpretation import Interpretation
from flloat.base.Symbol import Symbol, FunctionSymbol
from flloat.base.Symbols import Operators
from flloat.base.truths import Truth
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
            if item.operator == Operators.IN.value:
                return item.state in self.true_propositions
            elif item.operator == Operators.NOT_IN.value:
                return item.state not in self.true_propositions
            else:
                if item.norm == 'none':
                    for val in i:
                        result = eval(
                            '\'' + item.state + '\'' + ' ' + item.operator +
                            ' ' + '\'' + str(val) + '\''
                            )
                        if result is True:
                            return True
                    return False
                else:
                    setval = []
                    for v in self.true_propositions:
                        setval.append(list(v))

                    for k in range(len(setval[0])):
                        nlist = []
                        for llist in setval:
                            temp = llist[k]
                            nlist.append(np.float(temp))
                        array = np.array(nlist)
                        val = np.linalg.norm(array, ord=item.norm)
                        result = eval(
                            '\'' + item.state + '\'' + ' ' + item.operator +
                            ' ' + '\'' + str(val) + '\''
                            )
                        if result is True:
                            return True
                    return False

                # if item.norm == 'none':
                #    for val in self.true_propositions:
                #        result = eval(
                #            item.state + ' ' + item.operator +
                #            ' ' + val
                #            )
                #        if result is True:
                #            return True
                #    return False
                # Need to compute norm
                # else:
                #    print('from interpretations', self.true_propositions)
                #    pass
        except AttributeError:
            return item in self.true_propositions

    def __iter__(self):
        return self.true_propositions.__iter__()

    def __len__(self):
        return len(self.true_propositions)

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
               "\n\t".join(
                   "%d: {" % i + ", ".join(
                       map(
                           str, sorted(
                               e))) + "}" for i, e in enumerate(self.trace))


class FiniteTraceTruth(Truth):
    @abstractmethod
    def truth(self, i: FiniteTrace, pos: int):
        raise NotImplementedError



class FiniteTraceDict(Interpretation, dict):
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

    @staticmethod
    def fromDictSets(d: dict):
        #return FiniteTrace(
        #    [PLGInterpretation(frozenset(
        #
        # print ([{Symbol(string) for string in i[1]} for i in d.items()])
        # d1 = dict([])

        # for items in d.items():
        #     for i in range(len(items[1])):
        #         d[items[0]][i] = Symbol(d[items[0]][i])
        #     #d[items[0]] = set(d[items[0]])
        #     d[items[0]] = PLGInterpretation(frozenset(d[items[0]]))

        # return FiniteTrace(
        #    [PLGInterpretation(frozenset(d))]
        #)
        return d

        #return FiniteTraceDict([d])


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
               "\n\t".join(
                   "%d: {" % i + ", ".join(
                       map(
                           str, sorted(
                               e))) + "}" for i, e in enumerate(self.trace))
