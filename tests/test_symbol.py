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
    # formula = "P_[a,b,c,d][3,none,<=]"
    formula = "P_[a,b,c,d][3,||.||,<=]"
    parsed_form = parser(formula)
    sym = FunctionSymbol(formula)
    sym._parse()
    print(parsed_form)
    # assert parsed_formula == LTLfRelease([a, b])
    # assert parsed_formula.truth(t1) is True
    assert 5 == 4
