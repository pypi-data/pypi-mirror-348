"""
# Public Fault Tree Analyser: boolean.py

Classes pertaining to inversion-free Boolean algebra.

**Copyright 2025 Conway.**
Licensed under the GNU General Public License v3.0 (GPL-3.0-only).
This is free software with NO WARRANTY etc. etc., see LICENSE.
"""

import itertools
from typing import Optional

from pfta.utilities import concrete_combinations
from pfta.woe import ImplementationError


class Term:
    """
    A minimal cut set (or mode failure), represented as a Boolean product of events, i.e. a term.

    A Boolean term (i.e. conjunction (AND) of events) is encoded in binary,
    with the nth bit set if and only if the nth event is present as a factor.

    Note that 0 encodes an empty conjunction, which is True.
    """
    __slots__ = ('encoding',)

    encoding: int

    def __init__(self, encoding: int):
        self.encoding = encoding

    def __eq__(self, other):
        return self.encoding == other.encoding

    def __lt__(self, other):
        return (self.order(), self.encoding) < (other.order(), other.encoding)

    def __truediv__(self, other) -> 'Term':
        """
        Compute the result of removing from the numerator (self) all factors in the denominator (other).
        """
        return Term(self.encoding & ~other.encoding)

    def __hash__(self):
        return self.encoding

    def __repr__(self):
        return f'Term({bin(self.encoding)})'

    def order(self) -> int:
        return self.encoding.bit_count()

    def is_vacuous(self) -> bool:
        return self.encoding == 0

    def event_indices(self) -> tuple[int, ...]:
        """
        Extract the event indices, which are the set bits of the encoding.
        """
        return tuple(
            index
            for index, digit in enumerate(bin(self.encoding)[-1:1:-1])  # stop at 1 to avoid `0b` prefix
            if digit == '1'
        )

    def factors(self) -> tuple['Term', ...]:
        return tuple(
            Term.create_from_event_index(event_index)
            for event_index in self.event_indices()
        )

    def implies(self, other: 'Term') -> bool:
        """
        Decide whether a term implies another.

        Equivalent to deciding whether the term is a multiple of the other term.
        If so, the term would be redundant in a disjunction (OR) with the other term, as per the absorption law.

        For the term to be a multiple of the other term, all bits set in the other term must be set in the term.
        Thus, if there exists a bit not set in the term that is set in the other term, return False.
        """
        return ~self.encoding & other.encoding == 0

    @staticmethod
    def create_from_event_index(event_index: int) -> 'Term':
        encoding = 1 << event_index
        return Term(encoding)

    @staticmethod
    def conjunction(*terms: 'Term') -> 'Term':
        """
        Compute the conjunction (AND) of a sequence of terms.

        Since a factor is present in a conjunction if and only if it is present in at least one of the inputs,
        the conjunction encoding is the bitwise OR of the input term encodings.
        """
        conjunction_encoding = 0  # True

        for term in terms:
            conjunction_encoding |= term.encoding

        return Term(conjunction_encoding)

    @staticmethod
    def disjunction(*terms: 'Term') -> 'Expression':
        """
        Compute the disjunction (OR) of a sequence of terms.

        Since we only encounter coherent (NOT-free) logic, the result is merely an expression
        with the redundant terms removed as per the absorption law.
        """
        undecided_terms = set(terms)
        necessary_terms = set()

        while undecided_terms:
            term = undecided_terms.pop()

            for other_term in undecided_terms.copy():
                if term.implies(other_term):  # term is redundant
                    break

                if other_term.implies(term):  # other term is redundant
                    undecided_terms.discard(other_term)

            else:  # term is not redundant (because `break` not executed)
                necessary_terms.add(term)

        return Expression(*necessary_terms)

    @staticmethod
    def gcd(*terms: 'Term') -> 'Term':
        """
        Compute the greatest common divisor of a sequence of terms.
        """
        try:
            gcd_encoding = terms[0].encoding
        except IndexError:
            raise ValueError('cannot take gcd of an empty sequence of terms')

        for term in terms[1:]:
            gcd_encoding &= term.encoding

        return Term(gcd_encoding)


class Expression:
    """
    A general disjunction (OR) of minimal cut sets, represented as a Boolean sum of products, i.e. an expression.

    The constructor does not eliminate redundant terms. Use `Term.disjunction` for that purpose.

    Note that an empty disjunction is False.
    """
    __slots__ = ('terms',)

    terms: frozenset[Term]

    def __init__(self, *terms: Term):
        self.terms = frozenset([*terms])

    def __eq__(self, other):
        return self.terms == other.terms

    def __repr__(self):
        return f'Expression({", ".join(repr(t) for t in self.terms)})'

    def encodings(self) -> frozenset[int]:
        return frozenset(term.encoding for term in self.terms)

    def sole_term_encoding(self) -> Optional[int]:
        if not self.terms:  # expression is False
            return None

        if len(self.terms) != 1:
            raise ImplementationError(f'`{self}` does not have a sole term')

        return next(iter(self.terms)).encoding

    def substitute_true(self, event_index: int) -> 'Expression':
        """
        Substitute `True` for the event of the given index.

        Equivalent to dividing through all terms by the event.
        """
        vanisher = Term.create_from_event_index(event_index)

        return Term.disjunction(*(
            term / vanisher
            for term in self.terms
        ))

    def substitute_false(self, event_index: int) -> 'Expression':
        """
        Substitute `False` for the event of the given index.

        Equivalent to removing terms that contain the event.
        Elimination of redundant terms is not required, assuming the expression is already minimal.
        """
        return Expression(*(
            term
            for term in self.terms
            if event_index not in term.event_indices()
        ))

    def filter_terms(self, event_index: int) -> 'Expression':
        """
        Filter through terms, retaining only those that contain (as a factor) the event of the given index.

        Effectively the complement of `substitute_false`.
        """
        return Expression(*(
            term
            for term in self.terms
            if event_index in term.event_indices()
        ))

    @staticmethod
    def conjunction(*expressions: 'Expression') -> 'Expression':
        """
        Compute the conjunction (AND) of a sequence of expressions.

        This involves summing (disjunction) over the products (conjunction) of the Cartesian combinations of terms,
        as per the distributive law.
        """
        return Term.disjunction(*(
            Term.conjunction(*terms)
            for terms in itertools.product(*(expression.terms for expression in expressions))
        ))

    @staticmethod
    def disjunction(*expressions: 'Expression') -> 'Expression':
        """
        Compute the disjunction (OR) of a sequence of expressions.
        """
        return Term.disjunction(*(
            term
            for expression in expressions
            for term in expression.terms
        ))

    @staticmethod
    def vote(*input_expressions: 'Expression', threshold: int) -> 'Expression':
        """
        Compute the vote of a sequence of expressions.
        """
        return Expression.disjunction(*(
            Expression.conjunction(*combo)
            for combo in concrete_combinations(input_expressions, threshold)
        ))
