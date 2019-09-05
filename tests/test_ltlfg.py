from flloat.base.Symbol import Symbol, FunctionSymbol
from flloat.base.Symbols import Symbols, Operators
from flloat.parser.ltlfg import LTLfGParser
from flloat.parser.ltlf import LTLfParser

from flloat.semantics.ltlfg import FiniteTrace

from flloat.semantics.ltlfg import PLGInterpretation, PLGTrueInterpretation

from flloat.syntax.ltlfg import (
    LTLfgAtomic, LTLfAnd, LTLfEquivalence, LTLfOr, LTLfNot, LTLfImplies,
    LTLfEventually, LTLfAlways, LTLfUntil, LTLfRelease, LTLfNext,
    LTLfWeakNext, LTLfTrue, LTLfFalse
)


def test_parser():
    parser = LTLfGParser()
    a, b, c = [LTLfgAtomic(FunctionSymbol(c)) for c in "ABC"]
    print(type(parser("!A | B <-> !(A & !B) <-> A->B")))
    print(type(LTLfEquivalence([
        LTLfOr([LTLfNot(a), b]),
        LTLfNot(LTLfAnd([a, LTLfNot(b)])),
        LTLfImplies([a, b])
    ])))
    assert parser("!A | B <-> !(A & !B) <-> A->B") == LTLfEquivalence([
        LTLfOr([LTLfNot(a), b]),
        LTLfNot(LTLfAnd([a, LTLfNot(b)])),
        LTLfImplies([a, b])
    ])

    assert parser("(X A) & (WX !B)") == LTLfAnd([
        LTLfNext(a),
        LTLfWeakNext(LTLfNot(b))
    ])

    assert parser("(F (A&B)) <-> !(G (!A | !B) )") == LTLfEquivalence([
        LTLfEventually(LTLfAnd([a, b])),
        LTLfNot(LTLfAlways(LTLfOr([LTLfNot(a), LTLfNot(b)])))
    ])

    assert parser("(A U B U C) <-> !(!A R !B R !C)") == LTLfEquivalence([
        LTLfUntil([a, b, c]),
        LTLfNot(LTLfRelease([LTLfNot(a), LTLfNot(b), LTLfNot(c)]))
    ])


def test_truth():
    parser = LTLfGParser()
    t = FiniteTrace.fromStringSets([
        {"A"},
        {"A"},
        {"B"},
        {"B"},
        {"C"},
        {"C"},
    ])

    # Next and Weak Next
    f = "X A"
    assert parser("X A").truth(t, 0)
    assert not parser("X A").truth(t, 1)
    assert not parser("WX A").truth(t, 1)
    assert parser("X B").truth(t, 1)
    assert parser("X C").truth(t, 4)
    # at the last step, Next != WeakNext
    assert not parser("X C").truth(t, 5)
    assert parser("WX C").truth(t, 5)

    # Until
    f = "A U B U C"
    assert parser(f).truth(t, 0)
    assert parser(f).truth(t, 2)
    assert parser(f).truth(t, 4)
    assert not parser(f).truth(t, 10)

    assert not parser("A U C").truth(t, 0)
    assert not parser("C U B").truth(t, 0)

    # Release - dual of Until
    f = "(!A R !B R !C)"
    assert not parser(f).truth(t, 0)
    assert not parser(f).truth(t, 2)
    assert not parser(f).truth(t, 4)
    assert parser(f).truth(t, 10)

    assert not parser("A U C").truth(t, 0)
    assert not parser("C U B").truth(t, 0)

    # Eventually
    assert parser("F C & !A & !B").truth(t, 0)
    assert not parser("F A & B & C").truth(t, 0)
    assert parser("F G C").truth(t, 0)
    assert not parser("F G B").truth(t, 0)

    # Always
    assert parser("G A | B | C").truth(t, 0)
    assert parser("G F (C & !A & !B)").truth(t, 0)
    assert not parser("G C").truth(t, 0)
    assert parser("G C").truth(t, 4)
    assert parser("G C").truth(t, 10)
    assert parser("G F C").truth(t, 0)


def test_nnf():
    parser = LTLfGParser()
    a, b, c = [LTLfgAtomic(Symbol(c)) for c in "ABC"]

    f = parser("!(A & !B)")
    assert f.to_nnf() == LTLfOr([LTLfNot(a), b])

    f = parser("!(!A | B)")
    assert f.to_nnf() == LTLfAnd([a, LTLfNot(b)])

    f = parser("!( (A->B) <-> (!A | B))")
    assert f.to_nnf() == LTLfAnd([
        LTLfAnd([a, LTLfNot(b)]),
        LTLfOr([LTLfNot(a), b]),
    ])

    # Next and Weak Next
    f = parser("!(X (A & B))")
    assert f.to_nnf() == LTLfWeakNext(LTLfOr([LTLfNot(a), LTLfNot(b)]))

    f = parser("!(WX (A & B))")
    assert f.to_nnf() == LTLfNext(LTLfOr([LTLfNot(a), LTLfNot(b)]))

    # Eventually and Always
    f = parser("!(F (A | B))")
    assert f.to_nnf() == LTLfAlways(LTLfAnd([LTLfNot(a), LTLfNot(b)])).to_nnf()

    f = parser("!(F (A | B))")
    assert f.to_nnf() == LTLfAlways(LTLfAnd([LTLfNot(a), LTLfNot(b)])).to_nnf()
    f = parser("!(G (A | B))")
    assert f.to_nnf() == LTLfEventually(
        LTLfAnd([LTLfNot(a), LTLfNot(b)])).to_nnf()

    # Until and Release
    f = parser("!(A U B)")
    assert f.to_nnf() == LTLfRelease([LTLfNot(a), LTLfNot(b)])
    f = parser("!(A R B)")
    assert f.to_nnf() == LTLfUntil([LTLfNot(a), LTLfNot(b)])
