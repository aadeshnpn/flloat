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


def test_ltlfg_symbol():
    parser = LTLfGParser()
    # formula = "P_[a,b,c,d][3,none,<=]"
    formula = "P_[a,b,c,d][3,||.||,<=]"
    parsed_form = parser(formula)
    sym = FunctionSymbol(formula)
    sym._parse()
    assert sym.keys == ['a','b','c','d']
    assert sym.state == '3'
    assert sym.operator == '<='


def test_ltlfg_norm():
    parser = LTLfGParser()
    formula = "P_[x,y][0,|.|2,<=]"
    x = FiniteTrace.fromStringSets([
        {'0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '2',
         '2', '2', '2', '2', '3', '3', '3', '3', '3', '4', '4'}
    ])

    y = FiniteTrace.fromStringSets([
        {'0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '2',
         '2', '2', '2', '2', '3', '3', '3', '3', '3', '4', '4'}
    ])

    t1  = FiniteTraceDict.fromDictSets(
        {'x': x, 'y': y}
    )

    parsed_formula = parser(formula)
    sym = FunctionSymbol(formula)
    sym._parse()
    assert parsed_formula.truth(t1) is True
