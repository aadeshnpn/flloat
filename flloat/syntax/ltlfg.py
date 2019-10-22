from abc import abstractmethod
from functools import lru_cache
from typing import Set

from flloat.base.Formula import (
    Formula, CommutativeBinaryOperator, AtomicGFormula,
    BinaryOperator, UnaryOperator
    )
from flloat.base.Symbol import Symbol, FunctionSymbol
from flloat.base.Symbols import Symbols
from flloat.base.convertible import (
    ImpliesDeltaConvertible, EquivalenceDeltaConvertible, ConvertibleFormula,
    BaseConvertibleFormula, DeltaConvertibleFormula
    )
from flloat.base.nnf import (
    NNF, NotNNF, DualBinaryOperatorNNF, DualUnaryOperatorNNF
    )
from flloat.base.truths import Truth, NotTruth, OrTruth, AndTruth
from flloat.utils import MAX_CACHE_SIZE

# from flloat.flloat import DFAOTF, to_automaton, to_automaton_

from flloat.semantics.ltlfg import FiniteTrace, FiniteTraceTruth
from flloat.semantics.ltlfg import PLGInterpretation, PLGFalseInterpretation

from flloat.syntax.ldlf import (
    Delta,
    LDLfAtomic, LDLfNot, LDLfAnd, LDLfOr, LDLfEquivalence, LDLfDiamond,
    RegExpPropositional, RegExpStar, RegExpSequence, RegExpTest,
    LDLfPropositional, LDLfBox, LDLfEnd
    )

from flloat.syntax.pl import PLTrue, PLFalse, PLAnd, PLOr, PLAtomic, PLGAtomic


class LTLfgTruth(Truth):
    @abstractmethod
    def truth(self, i: FiniteTrace, pos: int = 0):
        raise NotImplementedError


class LTLfgFormula(Formula, LTLfgTruth, NNF, Delta):

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def delta(self, i: PLGInterpretation, epsilon=False):
        f = self.to_nnf()
        # f = self.to_LDLf().to_nnf()
        d = f._delta(i, epsilon)
        if epsilon:
            # By definition, if epsilon=True, then the result
            # must be either PLTrue or PLFalse
            # Now, the output is a Propositional Formula
            # with only PLTrue or PLFalse as atomics
            # Hence, we just evaluate the formula with a dummy PLInterpretation
            d = PLTrue() if d.truth(None) else PLFalse()
        return d

    @abstractmethod
    def _delta(self, i: PLGInterpretation, epsilon=False):
        """apply delta function, assuming that 'self' is a
        LTLf formula in Negative Normal Form"""
        raise NotImplementedError

    @abstractmethod
    def to_LDLf(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    # def to_automaton(
    #     self, labels: Set[Symbol]=None, on_the_fly=False,
    #         determinize=False, minimize=True):
    #     if labels is None:
    #         labels = self.find_labels()
    #     if on_the_fly:
    #         return DFAOTF(self)
    #     elif determinize:
    #         return to_automaton(self, labels, minimize)
    #     else:
    #         return to_automaton_(self, labels)


class LTLfCommBinaryOperator(CommutativeBinaryOperator, LTLfgFormula):
    pass


class LTLfTemporalFormula(LTLfgFormula, FiniteTraceTruth):
    pass


class LTLfgAtomic(AtomicGFormula, LTLfgFormula):

    def __init__(self, s: FunctionSymbol):
        AtomicGFormula.__init__(self, s)
        self.a = PLGAtomic(s)

    def __str__(self):
        return AtomicGFormula.__str__(self)

    def _members(self):
        return (LTLfgAtomic, self.s)

    def _to_nnf(self):
        return self

    def negate(self):
        return LTLfNot(LTLfgAtomic(self.s))

    def _delta(self, i: PLGInterpretation, epsilon=False):
        if epsilon:
            return PLFalse()
        return PLTrue() if self.a.truth(i) else PLFalse()

    def truth(self, i: FiniteTrace, pos: int=0):
        return self.a.truth(i.get(pos))

    def find_labels(self):
        return self.a.find_labels()

    def to_LDLf(self):
        return LDLfPropositional(self.a)._convert()


class LTLfTrue(LTLfgAtomic):
    def __init__(self):
        super().__init__(FunctionSymbol(Symbols.TRUE.value))
        self.a = PLTrue()

    def negate(self):
        return LTLfFalse()


class LTLfFalse(LTLfgAtomic):
    def __init__(self):
        super().__init__(FunctionSymbol(Symbols.FALSE.value))
        self.a = PLFalse()

    def negate(self):
        return LTLfTrue()


class LTLfNot(NotTruth, LTLfgFormula, NotNNF):

    def _delta(self, i: PLGInterpretation, epsilon=False):
        if isinstance(self.f, LTLfgAtomic) or isinstance(self.f, LTLfEnd):
            return PLTrue(
            ) if self.f._delta(i, epsilon) == PLFalse() else PLFalse()
        else:
            # the formula must be in NNF form!!!
            raise Exception

    def to_LDLf(self):
        return LDLfNot(self.f.to_LDLf())


class LTLfAnd(LTLfCommBinaryOperator, AndTruth, DualBinaryOperatorNNF):

    def _delta(self, i: PLGInterpretation, epsilon=False):
        return PLAnd([f._delta(i, epsilon) for f in self.formulas])

    def to_LDLf(self):
        return LDLfAnd([f.to_LDLf() for f in self.formulas])


class LTLfOr(LTLfCommBinaryOperator, OrTruth, DualBinaryOperatorNNF):

    def _delta(self, i: PLGInterpretation, epsilon=False):
        return PLOr([f._delta(i, epsilon) for f in self.formulas])

    def to_LDLf(self):
        return LDLfOr([f.to_LDLf() for f in self.formulas])


class LTLfImplies(ImpliesDeltaConvertible, LTLfgFormula):
    And = LTLfAnd
    Or = LTLfOr
    Not = LTLfNot

    def to_LDLf(self):
        return self._convert().to_LDLf()


class LTLfEquivalence(EquivalenceDeltaConvertible, LTLfCommBinaryOperator):
    And = LTLfAnd
    Or = LTLfOr
    Not = LTLfNot

    def to_LDLf(self):
        return self._convert().to_LDLf()


class LTLfNext(DualUnaryOperatorNNF, LTLfTemporalFormula):
    operator_symbol = "X"
    Not = LTLfNot

    def truth(self, i: FiniteTrace, pos: int=0):
        if type(i).__name__ == 'dict':
            i = FiniteTrace.fromStringSets(i[self.f.s.key])
        return pos < i.last() and self.f.truth(i, pos + 1)

    def _delta(self, i: PLGInterpretation, epsilon=False):
        if epsilon:
            return PLFalse()
        else:
            return PLAnd([self.f, LTLfNot(LTLfEnd()).to_nnf()])

    def to_LDLf(self):
        return LDLfDiamond(
            RegExpPropositional(PLTrue()), LDLfAnd(
                [self.f.to_LDLf(), LDLfNot(LDLfEnd())]))


class LTLfWeakNext(
        DualUnaryOperatorNNF, ConvertibleFormula, LTLfTemporalFormula):
    operator_symbol = Symbols.WEAK_NEXT.value
    Not = LTLfNot

    def _convert(self):
        return LTLfNot(LTLfNext(LTLfNot(self.f)))

    def truth(self, i: FiniteTrace, pos: int=0):
        if type(i).__name__ == 'dict':
            i = FiniteTrace.fromStringSets(i[self.f.s.key])
        return self._convert().truth(i, pos)

    def _delta(self, i: PLGInterpretation, epsilon=False):
        if epsilon:
            return PLTrue()
        else:
            return PLOr([self.f, LTLfEnd().to_nnf()])
            # return LTLfOr([self.f, LTLfWeakNext(LTLfFalse())])

            # if self.f == LTLfFalse():
            #     return LTLfFalse()
            # return PLOr([self.f, LTLfWeakNext(LTLfFalse())])

    def to_LDLf(self):
        return self._convert().to_LDLf()


class LTLfUntil(DualBinaryOperatorNNF, LTLfTemporalFormula):
    operator_symbol = "U"

    def _to_nnf(self):
        return LTLfUntil([f.to_nnf() for f in self.formulas])

    def negate(self):
        return LTLfRelease([LTLfNot(f) for f in self.formulas])

    def truth(self, i: FiniteTrace, pos: int=0):
        f1 = self.formulas[0]
        f2 = LTLfUntil(
            self.formulas[1:]) if len(self.formulas) > 2 else self.formulas[1]
        print(f1, f2)
        if type(i).__name__ == 'dict':
            #, 'LTLfTrue', 'LTLfFalse'):
            if type(f1).__name__ == LTLfgAtomic.__name__:
                i1 = FiniteTrace.fromStringSets(i[f1.s.key])
            elif type(f1).__name__ in ('LTLfTrue', 'LTLfFalse'):
                i1 = FiniteTrace.fromStringSets(i[list(i.keys())[0]])
            else:
                i1 = FiniteTrace.fromStringSets(i[f1.f.s.key])
            print(type(f2))
            if type(f2).__name__ == LTLfUntil.__name__:
                i2 = i
            else:
                if type(f2).__name__ == LTLfgAtomic.__name__:
                    i2 = FiniteTrace.fromStringSets(i[f2.s.key])
                elif type(f2).__name__ in ('LTLfTrue', 'LTLfFalse'):
                    i2 = FiniteTrace.fromStringSets(i[list(i.keys())[0]])
                elif type(f2).__name__ in ('LTLfAnd'):
                    print(dir(f2))
                    i2 = i # print('ltlfand',dir(f2))
                else:
                    try:
                        i2 = FiniteTrace.fromStringSets(i[f2.f.s.key])
                    except AttributeError:
                        i2 = i1
        else:
            i1, i2 = i, i

        # b = all(
        #    f1.truth(i1, k) for j in range(
        #        pos, i1.last()+1) for k in range(pos, j))

        # a = any(f2.truth(i2, j) for j in range(pos, i1.last()+1))
        print('i1, i2',i1, i2)
        return any(
            f2.truth(i2, j) and all(
                f1.truth(i1, k) for k in range(
                    pos, j)) for j in range(pos, i1.last()+1))

    def _delta(self, i: PLGInterpretation, epsilon=False):
        if epsilon:
            return PLFalse()
        f1 = self.formulas[0]
        f2 = LTLfUntil(
            self.formulas[1:]) if len(self.formulas) > 2 else self.formulas[1]
        return PLOr([
            f2._delta(i, epsilon),
            PLAnd([
                f1._delta(i, epsilon),
                LTLfNext(self)._delta(i, epsilon)
            ])
        ])

    def to_LDLf(self):
        f1 = self.formulas[0].to_LDLf()
        f2 = LTLfUntil(
            self.formulas[1:]).to_LDLf() if len(
                self.formulas) > 2 else self.formulas[1].to_LDLf()
        return LDLfDiamond(
            RegExpStar(RegExpSequence(
                [RegExpTest(f1), RegExpPropositional(
                    PLTrue())])), LDLfAnd([f2, LDLfNot(LDLfEnd())]))


class LTLfEventually(
        UnaryOperator, DeltaConvertibleFormula, LTLfTemporalFormula):
    operator_symbol = "F"
    Not = LTLfNot

    def _convert(self):
        return LTLfUntil([LTLfTrue(), self.f])

    # def _delta(self, i:PLInterpretation, epsilon=False):
        # if epsilon:
        #     return PLFalse()
        # else:
        #     return PLOr([self.f._delta(
        # i, epsilon), LTLfNext(self)._delta(i, epsilon)])

    def to_LDLf(self):
        # return self._convert().to_LDLf()
        return LDLfDiamond(
            RegExpStar(RegExpPropositional(
                PLTrue())), LDLfAnd([self.f.to_LDLf(), LDLfNot(LDLfEnd())]))


class LTLfAlways(UnaryOperator, DeltaConvertibleFormula, LTLfTemporalFormula):
    operator_symbol = "G"
    Not = LTLfNot

    def _convert(self):
        return LTLfNot(LTLfEventually(LTLfNot(self.f))._convert())

    # def _delta(self, i:PLGInterpretation, epsilon=False):
    #     if epsilon:
    #         return PLTrue()
    #     else:
    #         return PLAnd([self.f._delta(
    # i, epsilon), LTLfWeakNext(self)._delta(i, epsilon)])

    def to_LDLf(self):
        return self._convert().to_LDLf()


class LTLfRelease(
        DualBinaryOperatorNNF, BaseConvertibleFormula, LTLfTemporalFormula):
    operator_symbol = "R"
    Dual = LTLfUntil

    def _convert(self):
        return LTLfNot(LTLfUntil([LTLfNot(f) for f in self.formulas]))

    def _delta(self, i: PLGInterpretation, epsilon=False):
        if epsilon:
            return PLTrue()
        f1 = self.formulas[0]
        f2 = LTLfRelease(
            self.formulas[1:]) if len(self.formulas) > 2 else self.formulas[1]
        return PLAnd([
            f2._delta(i, epsilon),
            PLOr([
                f1._delta(i, epsilon),
                LTLfWeakNext(self)._delta(i, epsilon)
            ])
        ])

    def to_LDLf(self):
        return self._convert().to_LDLf()


class LTLfEnd(DeltaConvertibleFormula, BaseConvertibleFormula, LTLfgAtomic):
    def __init__(self):
        LTLfgAtomic.__init__(self, Symbol("End"))

    def _members(self):
        return (self.s, )

    def _convert(self):
        return LTLfAlways(LTLfFalse()).to_nnf()

    def negate(self):
        return LTLfEventually(LTLfTrue()).to_nnf()

    def __str__(self):
        return "_".join(map(str, self._members()))


LTLfAnd.Dual = LTLfOr
LTLfOr.Dual = LTLfAnd

LTLfNext.Dual = LTLfWeakNext
LTLfWeakNext.Dual = LTLfNext

LTLfEventually.Dual = LTLfAlways
LTLfAlways.Dual = LTLfEventually
