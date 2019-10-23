from flloat.base.Symbol import Symbol, FunctionSymbol
from flloat.base.Symbols import Symbols, Operators
from flloat.parser.ltlfg import LTLfGParser
# from flloat.parser.ltlf import LTLfParser

from flloat.semantics.ltlfg import FiniteTrace, FiniteTraceDict

from flloat.semantics.ltlfg import (
    PLGInterpretation, PLGTrueInterpretation, PLGFalseInterpretation
)

from flloat.syntax.ltlfg import (
    LTLfgAtomic, LTLfAnd, LTLfEquivalence, LTLfOr, LTLfNot, LTLfImplies,
    LTLfEventually, LTLfAlways, LTLfUntil, LTLfRelease, LTLfNext,
    LTLfWeakNext, LTLfTrue, LTLfFalse
)

from flloat.syntax.pl import PLGAtomic, PLTrue, PLFalse, PLAnd, PLOr


def test_ltlfg_mdp():
    parser = LTLfGParser()
    formula = "P_s[S11,in] R P_s[S88,in]"
    parsed_formula = parser(formula)
    a = LTLfgAtomic(FunctionSymbol('P_s[S11,in]'))
    b = LTLfgAtomic(FunctionSymbol('P_s[S88,in]'))
    # S and E are action. S11.. are states. The MDP world is 8x8

    t1 = FiniteTrace.fromStringSets(
        [{'S11', 'S', 'S21', 'E', 'S22', 'E', 'S23', 'E', 'S24',
        'E', 'S25', 'E', 'S26', 'E', 'S27', 'S', 'S37',
        'S', 'S47', 'S', 'S57', 'S', 'S67', 'E', 'S68',
        'S', 'S78', 'S', 'S88'}]
    )
    t1  = FiniteTraceDict.fromDictSets(
        {'s': t1}
    )
    assert parsed_formula == LTLfRelease([a, b])
    assert parsed_formula.truth(t1) is True


def test_ltlfg_mdp_trace():
    parser = LTLfGParser()
    formula = "P_s[S11,in] R P_s[S88,in]"
    parsed_formula = parser(formula)
    a = LTLfgAtomic(FunctionSymbol('P_s[S11,in]'))
    b = LTLfgAtomic(FunctionSymbol('P_s[S88,in]'))
    # S and E are action. S11.. are states. The MDP world is 8x8
    t1 = FiniteTrace.fromStringSets(
        [
        {'S11'},
        {'S11', 'S'},
        {'S11', 'S', 'E'},
        {'S11', 'S', 'E', 'S22'},
        {'S11', 'S', 'E', 'S22', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67', 'E'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67', 'E', 'S68'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67', 'E', 'S68', 'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67', 'E', 'S68', 'S',
         'S78'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67', 'E', 'S68', 'S',
         'S78', 'S'},
        {'S11', 'S', 'E', 'S22', 'E', 'S23', 'E', 'S24', 'S', 'S21', 'E',
         'S22', 'E', 'S23', 'E', 'S24', 'E', 'S25', 'E', 'S26', 'E', 'S27',
         'S', 'S37', 'S', 'S47', 'S', 'S57', 'S', 'S67', 'E', 'S68', 'S',
         'S78', 'S', 'S88'}
    ])

    t1  = FiniteTraceDict.fromDictSets(
        {'s': t1}
    )
    assert parsed_formula == LTLfRelease([a, b])
    assert parsed_formula.truth(t1) is False


def test_ltlfg_velocity():
    parser = LTLfGParser()
    formula = "P_v[19,<] R P_v[55,>]"
    parsed_formula = parser(formula)

    t1 = FiniteTrace.fromStringSets([
        {'20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
         '31', '32', '33', '34', '35', '36', '37', '50', '51', '52', '53'}
    ])

    t1  = FiniteTraceDict.fromDictSets(
        {'v': t1}
    )
    assert parsed_formula.truth(t1) is True


def test_ltlfg_set():
    parser = LTLfGParser()
    formula = "P_s[A,not_in] R P_s[B,not_in]"
    parsed_formula = parser(formula)

    t1 = FiniteTrace.fromStringSets([
        {'B', 'C', 'A'}
    ])

    t1  = FiniteTraceDict.fromDictSets(
        {'s': t1}
    )
    assert parsed_formula.truth(t1) is False


def test_parser():
    parser = LTLfGParser()
    a, b, c = [LTLfgAtomic(FunctionSymbol(c)) for c in "ABC"]
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
        {"C"}
    ])

    t = FiniteTraceDict.fromDictSets({'s': t})

    # Next and Weak Next
    f = "X P_s[A,in]"
    assert parser("X P_s[A,in]").truth(t, 0)
    assert not parser("X P_s[A,in]").truth(t, 1)
    assert not parser("WX P_s[A,in]").truth(t, 1)
    assert parser("X P_s[B,in]").truth(t, 1)
    assert parser("X P_s[C,in]").truth(t, 4)
    # at the last step, Next != WeakNext
    assert not parser("X P_s[C,in]").truth(t, 5)
    assert parser("WX P_s[C,in]").truth(t, 5)

    # Until
    f = "P_s[A,in] U P_s[B,in] U P_s[C,in]"
    assert parser(f).truth(t, 0)
    assert parser(f).truth(t, 2)
    assert parser(f).truth(t, 4)
    assert not parser(f).truth(t, 10)

    assert not parser("P_s[A,in] U P_s[C,in]").truth(t, 0)
    assert not parser("P_s[C,in] U P_s[B,in]").truth(t, 0)

    # Release - dual of Until
    f = "(P_s[A,not_in] R P_s[B,not_in] R P_s[C,not_in])"
    assert not parser(f).truth(t, 0)
    assert not parser(f).truth(t, 2)
    assert not parser(f).truth(t, 4)
    assert parser(f).truth(t, 10)

    assert not parser("P_s[A,in] U P_s[C,in]").truth(t, 0)
    assert not parser("P_s[A,in] U P_s[C,in]").truth(t, 0)

    # Eventually
    # assert parser("F (P_s[C,in] & P_s[A,not_in] & P_s[B,not_in])").truth(t, 0)
    assert not parser("F P_s[A,in] & P_s[B,in] & P_s[C,in]").truth(t, 0)
    assert parser("F G P_s[C,in]").truth(t, 0)
    assert not parser("F G P_s[B,in]").truth(t, 0)

    # Always
    assert parser("G P_s[A,in] | P_s[B,in] | P_s[C,in]").truth(t, 0)
    assert parser("G F (P_s[C,in] & P_s[A,not_in] & P_s[B,not_in])").truth(t, 0)
    assert not parser("G P_s[C,in]").truth(t, 0)
    assert parser("G P_s[C,in]").truth(t, 4)
    assert parser("G P_s[C,in]").truth(t, 10)
    assert parser("G F P_s[C,in]").truth(t, 0)


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


def test_delta():
    parser = LTLfGParser()
    sa, sb = FunctionSymbol("A"), FunctionSymbol("B")
    a, b = PLGAtomic(sa), PLGAtomic(sb)

    i_ = PLGFalseInterpretation()
    i_a = PLGInterpretation({sa})
    i_b = PLGInterpretation({sb})
    i_ab = PLGInterpretation({sa, sb})

    true = PLTrue()
    false = PLFalse()

    assert parser("A").delta(i_) == false
    assert parser("A").delta(i_a) == true
    assert parser("A").delta(i_b) == false
    assert parser("A").delta(i_ab) == true

    assert parser("!A").delta(i_) == true
    assert parser("!A").delta(i_a) == false
    assert parser("!A").delta(i_b) == true
    assert parser("!A").delta(i_ab) == false

    assert parser("A & B").delta(i_) == PLAnd([false, false])
    assert parser("A & B").delta(i_a) == PLAnd([true, false])
    assert parser("A & B").delta(i_b) == PLAnd([false, true])
    assert parser("A & B").delta(i_ab) == PLAnd([true, true])

    assert parser("A | B").delta(i_) == PLOr([false, false])
    assert parser("A | B").delta(i_a) == PLOr([true, false])
    assert parser("A | B").delta(i_b) == PLOr([false, true])
    assert parser("A | B").delta(i_ab) == PLOr([true, true])

    assert parser("X A").delta(
        i_) == PLAnd([LTLfgAtomic(sa), LTLfEventually(LTLfTrue()).to_nnf()])
    assert parser(
        "X A").delta(i_a) == PLAnd(
            [LTLfgAtomic(sa), LTLfEventually(LTLfTrue()).to_nnf()])
    assert parser(
        "X A").delta(i_b) == PLAnd(
            [LTLfgAtomic(sa), LTLfEventually(LTLfTrue()).to_nnf()])
    assert parser(
        "X A").delta(i_ab) == PLAnd(
            [LTLfgAtomic(sa), LTLfEventually(LTLfTrue()).to_nnf()])
    assert parser("X A").delta(i_, epsilon=True) == false
    assert parser(
        "F A").delta(i_a) == PLOr([true,  PLAnd(
            [LTLfEventually(
                LTLfTrue()).to_nnf(), true, LTLfUntil(
                    [LTLfTrue(), LTLfgAtomic(sa)])])])
    assert parser(
        "F A").delta(i_) == PLOr(
            [false, PLAnd([LTLfEventually(
                LTLfTrue()).to_nnf(), true, LTLfUntil(
                    [LTLfTrue(), LTLfgAtomic(sa)])])])
    assert parser("F A").delta(i_a, epsilon=True) == false
    assert parser("F A").delta(i_, epsilon=True) == false

    assert parser(
        "G A").delta(i_a) == PLAnd(
            [true, PLOr(
                [false, LTLfAlways(
                    LTLfFalse()).to_nnf(), LTLfRelease(
                        [LTLfFalse(), LTLfgAtomic(sa)])])])
    assert parser(
        "G A").delta(i_a) == PLAnd(
            [true, PLOr([false, LTLfAlways(
                LTLfFalse()).to_nnf(), LTLfRelease(
                    [LTLfFalse(), LTLfgAtomic(sa)])])])
    assert parser("G A").delta(i_a, epsilon=True) == true
    assert parser("G A").delta(i_,  epsilon=True) == true

    assert parser("A U B").delta(i_a) == PLOr([
        false,
        PLAnd([
            true,
            LTLfUntil([LTLfgAtomic(sa), LTLfgAtomic(sb)]),
            LTLfEventually(LTLfTrue()).to_nnf()
        ])
    ])

    assert parser("A R B").delta(i_a) == PLAnd([
        false,
        PLOr([
            true,
            LTLfRelease([LTLfgAtomic(sa), LTLfgAtomic(sb)]),
            LTLfAlways(LTLfFalse()).to_nnf()
        ])
    ])
