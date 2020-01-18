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
    formula = "P_[a,b,c,d][3,||.||,<=,00]"
    parsed_form = parser(formula)
    sym = FunctionSymbol(formula)
    sym._parse()
    assert sym.keys == ['a','b','c','d']
    assert sym.state == '3'
    assert sym.operator == '<='


def test_ltlfg_norm():
    parser = LTLfGParser()
    formula = "P_[x,y][0,|.|2,<=,00]"
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


def test_ltltf_real():
    t = [set(['31', '31', '21', '11', '10', '10', '11', '11', '11', '12', '13', '14', '14', '14', '24', '24', '24', '14', '04', '03', '02', '02', '02', '02', '02', '02', '02', '03', '03', '03', '02', '12', '13', '14', '14', '14', '04', '04', '04', '04', '03', '02', '12', '02', '03', '03', '03', '04', '04', '03', '02', '12', '12', '11', '10', '11', '01', '01', '01', '01', '00'])]
    goalspec = 'P_[T][00,none,==]'
    parser = LTLfGParser()

    # Define goal formula/specification
    parsed_formula = parser(goalspec)
    print(parsed_formula)
    tl = FiniteTrace.fromStringSets(t)
    t  = FiniteTraceDict.fromDictSets(
        {'T': tl}
    )
    #result = parsed_formula.truth(t)

    sym = FunctionSymbol(goalspec)
    sym._parse()
    assert sym.keys == ['T']
    assert sym.state == '00'
    assert sym.operator == '=='
    assert parsed_formula.truth(t) is True


def test_ltlfg_norm_cityblock():
    parser = LTLfGParser()
    formula = "P_[l][10,|.|city,==,00]"
    l = FiniteTrace.fromStringSets([
        {'01', '02', '03', '11', '12', '13', '21', '22',
         '23', '31', '32', '33'}
    ])

    t1  = FiniteTraceDict.fromDictSets(
        {'l': l}
    )

    parsed_formula = parser(formula)
    sym = FunctionSymbol(formula)
    sym._parse()
    assert parsed_formula.truth(t1) is False


def test_ltlfg_norm_origin():
    parser = LTLfGParser()
    formula = "P_[x,y][9,|.|2,<=,00]"
    x = FiniteTrace.fromStringSets([
        {'0', '1', '2'}
    ])

    y = FiniteTrace.fromStringSets([
        {'0', '1', '2'}
    ])

    t1  = FiniteTraceDict.fromDictSets(
        {'x': x, 'y': y}
    )

    parsed_formula = parser(formula)
    sym = FunctionSymbol(formula)
    sym._parse()
    assert parsed_formula.truth(t1) is False