# -*- coding: utf-8 -*-
"""Library wide enum classes."""

from enum import Enum


class Symbols(Enum):
    """Symbols class for LTL."""

    NOT = "!"
    AND = "&"
    OR = "|"
    EQUAL = "="
    IMPLIES = "->"
    EQUIVALENCE = "<->"
    NEXT = "X"
    WEAK_NEXT = "WX"
    UNTIL = "U"
    RELEASE = "R"
    EVENTUALLY = "F"
    ALWAYS = "G"
    PATH_UNION = "+"
    PATH_SEQUENCE = ";"
    PATH_STAR = "*"
    PATH_TEST = "?"
    ROUND_BRACKET_LEFT = "("
    ROUND_BRACKET_RIGHT = ")"
    EVENTUALLY_BRACKET_LEFT = "<"
    EVENTUALLY_BRACKET_RIGHT = ">"
    ALWAYS_BRACKET_LEFT = "["
    ALWAYS_BRACKET_RIGHT = "]"
    LAST = "last"
    END = "end"
    LOGICAL_TRUE = "tt"
    LOGICAL_FALSE = "ff"
    CARET = "^"
    TRUE = "true"
    FALSE = "false"
    LTLf_LAST = "last"


class Operators(Enum):
    """Operator class for predicate."""

    NOT_EQUALS = "!="
    EQUAL = "=="
    LESS = "<"
    LESS_EQUALS = "<="
    GREATER = ">"
    GREATER_EQUALS = ">="
    IN = "in"
    NOT_IN = "not_in"


ALL_SYMBOLS = {v.value for v in Symbols}
ALL_OPERATORS = {v.value for v in Operators}
