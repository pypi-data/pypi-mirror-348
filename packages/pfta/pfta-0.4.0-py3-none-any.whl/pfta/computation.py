"""
# Public Fault Tree Analyser: computation.py

Fault tree computational methods.

**Copyright 2025 Conway.**
Licensed under the GNU General Public License v3.0 (GPL-3.0-only).
This is free software with NO WARRANTY etc. etc., see LICENSE.
"""

import collections
import math
from typing import TYPE_CHECKING, Collection, DefaultDict, Iterable, Optional

from pfta.boolean import Term, Expression
from pfta.common import natural_repr
from pfta.utilities import robust_divide, descending_product, descending_sum, concrete_combinations

if TYPE_CHECKING:
    from pfta.core import Event


class ComputationalCache:
    """
    Class for caching laborious computations.
    """
    _q_from_index_from_encoding: DefaultDict[Optional[int], dict[int, float]]
    _omega_from_index_from_encoding: DefaultDict[Optional[int], dict[int, float]]
    _q_from_index_from_encodings: DefaultDict[frozenset[int], dict[int, float]]
    _omega_from_index_from_encodings: DefaultDict[frozenset[int], dict[int, float]]
    _combos_from_order_from_terms: DefaultDict[Collection[Term], dict[int, list[tuple[Term, ...]]]]
    truncation_tolerance: float
    truncation_order: Optional[int]

    def __init__(self, events: list['Event'], truncation_tolerance: float, truncation_order: Optional[int]):
        q_from_index_from_encoding = {
            event.computed_expression.sole_term_encoding(): dict(enumerate(event.computed_probabilities))
            for event in events
        }
        omega_from_index_from_encoding = {
            event.computed_expression.sole_term_encoding(): dict(enumerate(event.computed_intensities))
            for event in events
        }

        self._q_from_index_from_encoding = collections.defaultdict(dict, q_from_index_from_encoding)
        self._omega_from_index_from_encoding = collections.defaultdict(dict, omega_from_index_from_encoding)
        self._q_from_index_from_encodings = collections.defaultdict(dict)
        self._omega_from_index_from_encodings = collections.defaultdict(dict)
        self._combos_from_order_from_terms = collections.defaultdict(dict)
        self.truncation_tolerance = truncation_tolerance
        self.truncation_order = truncation_order

    def __repr__(self):
        return natural_repr(self, ellipsis_attributes=('truncation_tolerance', 'truncation_order'))

    def term_probability(self, term: Term, index: int) -> float:
        encoding = term.encoding

        if index not in self._q_from_index_from_encoding[encoding]:
            self._q_from_index_from_encoding[encoding][index] = uncached_term_probability(term, index, self)

        return self._q_from_index_from_encoding[encoding][index]

    def term_intensity(self, term: Term, index: int) -> float:
        encoding = term.encoding

        if index not in self._omega_from_index_from_encoding[encoding]:
            self._omega_from_index_from_encoding[encoding][index] = uncached_term_intensity(term, index, self)

        return self._omega_from_index_from_encoding[encoding][index]

    def term_rate(self, term: Term, index: int) -> float:
        q = self.term_probability(term, index)
        omega = self.term_intensity(term, index)

        return robust_divide(omega, 1 - q)

    def expression_probability(self, expression: Expression, index: int) -> float:
        encodings = expression.encodings()

        if index not in self._q_from_index_from_encodings[encodings]:
            probability = uncached_expression_probability(expression, index, self)
            self._q_from_index_from_encodings[encodings][index] = probability

        return self._q_from_index_from_encodings[encodings][index]

    def expression_intensity(self, expression: Expression, index: int) -> float:
        encodings = expression.encodings()

        if index not in self._omega_from_index_from_encodings[encodings]:
            intensity = uncached_expression_intensity(expression, index, self)
            self._omega_from_index_from_encodings[encodings][index] = intensity

        return self._omega_from_index_from_encodings[encodings][index]

    def term_combinations(self, terms: Collection[Term], order: int) -> list[tuple[Term, ...]]:
        if order not in self._combos_from_order_from_terms[terms]:
            self._combos_from_order_from_terms[terms][order] = concrete_combinations(terms, order)

        return self._combos_from_order_from_terms[terms][order]


def constant_rate_model_probability(t: float, lambda_: float, mu: float) -> float:
    """
    Instantaneous failure probability q(t) for a component with constant failure and repair rates λ and μ.

    Explicitly, q(t) = [λ/(λ+μ)] [1−exp(−(λ+μ)t)].

    |  λ  |  μ  |  t  |  q  | Explanation
    | --- | --- | --- | --- | -----------
    |  0  |  0  | i|n | nan | 0/0 [1−exp(−0.i|n)] = nan (since 0/0 is independent of i|n)
    |     |     | oth |  0  | λ/(λ+μ).(λ+μ)t = λt = 0
    |     | inf | any |  0  | 0/i [1−exp(−i.any)] = 0.finite = 0
    |     | nan | i|n | nan | {nan (per above) if μ=0}
    |     |     | oth |  0  | {0 (per above) if μ=0; 0/μ [1−exp(−μt)] = 0.finite = 0 if μ≠0}  # mergeable with next
    |     | oth | any |  0  | 0/μ [1−exp(−μ.any)] = 0.finite = 0
    | inf | i|n | any | nan | i/(i+i|n) [1−exp(−(i+i|n).any)] = nan.finite = nan
    |     | oth | 0|n | nan | 1 [1−exp(−inf.0|n)] = 1.nan = nan
    |     |     | oth |  1  | 1 [1−exp(−inf.t)] = 1.1 = 1
    | nan |  0  | i|n | nan | {nan (per above) if λ=0}
    |     |     | oth | nan | 1 [1−exp(−nan.t)] = nan                                         # mergeable with previous
    |     | i|n | any | nan | {nan (per above) if λ=inf}                                      # mergeable with previous
    |     | oth | any | nan | nan [1−exp(−nan.any)] = nan.finite = nan                        # mergeable with previous
    | oth | inf | any |  0  | λ/i [1−exp(−i.any)] = 0.finite = 0
    |     | nan | inf | nan | {0 (per above) if μ=inf; 1 [1−exp(−λ.inf)] = 1 if μ=0}
    |     |     | oth | nan | {0 (per above) if μ=inf; 1 [1−exp(−λ.t)] ≠ 0 if μ=0}            # mergeable with previous
    |     | oth | any | :-) | computable
    """
    if lambda_ == 0:
        if mu == 0:
            if math.isinf(t) or math.isnan(t):
                return float('nan')

            return 0.

        if math.isinf(mu):
            return 0.

        if math.isnan(mu):
            if math.isinf(t) or math.isnan(t):
                return float('nan')

        return 0.

    if math.isinf(lambda_):
        if math.isinf(mu) or math.isnan(mu):
            return float('nan')

        if t == 0 or math.isnan(t):
            return float('nan')

        return 1.

    if math.isnan(lambda_):
        return float('nan')

    if math.isinf(mu):
        return 0.

    if math.isnan(mu):
        return float('nan')

    return lambda_ / (lambda_ + mu) * -math.expm1(-(lambda_ + mu) * t)


def constant_rate_model_intensity(t: float, lambda_: float, mu: float) -> float:
    """
    Instantaneous failure intensity ω(t) for a component with constant failure and repair rates λ and μ.

    Explicitly, ω(t) = λ (1−q(t)), where q(t) is the corresponding failure probability.

    |  λ  |  μ  |  t  |  ω  | Explanation
    | --- | --- | --- | --- | -----------
    |  0  | any | any |  0  | 0 (1−q(t)) = 0.finite = 0
    | inf | i|n | any | nan | {i (1−q(t)) = i.1 = i if λ/μ=0; λ (1−[1−exp(−λ.t)]) = 0 if λ/μ=inf}
    |     | oth | 0|n | nan | i . 1 [1−exp(−i.0|n)] = nan (since i is independent of 0|n)
    |     |     | oth |  μ  | λ (1−λ/(λ+μ).1) = λ μ/(λ+μ) = μ
    | nan | i|n | any | nan | {nan (per above) if λ=inf}
    |     | oth | 0|n | nan | {nan (per above) if λ=inf}                                      # mergeable with previous
    |     |     | oth | nan | {0 (per above) if λ=0; μ (per above) if λ=inf}                  # mergeable with previous
    | oth | inf | any |  λ  | λ (1−q(t)) = λ.(1−0) = λ
    |     | nan | any | nan | λ (1−q(t)) = λ.(1−nan) = nan
    |     | oth | any | :-) | computable
    """
    if lambda_ == 0:
        return 0.

    if math.isinf(lambda_):
        if math.isinf(mu) or math.isnan(mu):
            return float('nan')

        if t == 0 or math.isnan(t):
            return float('nan')

        return mu

    if math.isnan(lambda_):
        return float('nan')

    if math.isinf(mu):
        return lambda_

    if math.isnan(mu):
        return float('nan')

    q = constant_rate_model_probability(t, lambda_, mu)
    return lambda_ * (1 - q)


def uncached_term_probability(term: Term, flattened_index: int, computational_cache: ComputationalCache) -> float:
    """
    Instantaneous failure probability of a Boolean term (representing a minimal cut set).

    From `MATHS.md`, the failure probability of a minimal cut set `C = x y z ...` is given by
        q[C] = q[x] q[y] q[z] ...
             = ∏{e|C} q[e],
    a straight product of the failure probabilities of its constituent primary events (i.e. factors).
    """
    def q(factor: Term) -> float:
        return computational_cache.term_probability(factor, flattened_index)

    return descending_product(q(factor) for factor in term.factors())


def uncached_term_intensity(term: Term, flattened_index: int, computational_cache: ComputationalCache) -> float:
    """
    Instantaneous failure intensity of a Boolean term (representing a minimal cut set).

    From `MATHS.md`, the failure intensity of a minimal cut set `C = x y z ...`
    is given by a product-rule-style expression, where each term is the product of
    one primary event's failure intensity and the remaining primary events' failure probabilities:
        ω[C] =   ω[x] q[y] q[z] ...
               + q[x] ω[y] q[z] ...
               + q[x] q[y] ω[z] ...
               + ...
             = ∑{e|C} ω[e] q[C ÷ e].
    """
    def q(factor: Term) -> float:
        return computational_cache.term_probability(factor, flattened_index)

    def omega(reduced_term: Term) -> float:
        return computational_cache.term_intensity(reduced_term, flattened_index)

    return descending_sum(
        omega(factor) * q(term / factor)
        for factor in term.factors()
    )


def uncached_expression_probability(expression: Expression, flattened_index: int,
                                    computational_cache: ComputationalCache) -> float:
    """
    Instantaneous failure probability for a general Boolean expression (a disjunction (OR) of terms).

    From `MATHS.md`, for a gate `T` represented as a disjunction of `N` minimal cut sets,
        T = C_1 + C_2 + ... + C_N,
    the failure probability `q[T]` of the top gate is given by the inclusion–exclusion principle,
        q[T] =   ∑{1≤i≤N} q[C_i]
               − ∑{1≤i<j≤N} q[C_i C_j]
               + ∑{1≤i<j<k≤N} q[C_i C_j C_k]
               − ... .
    In the implementation, we truncate if the truncation order is reached,
    or after the latest contribution divided by the partial sum falls below the truncation tolerance.
    """
    terms = expression.terms

    and_ = Term.conjunction
    combinations = computational_cache.term_combinations

    def q(term: Term) -> float:
        return computational_cache.term_probability(term, flattened_index)

    def q_contribution(order: int) -> float:
        return (
            (-1) ** (order - 1)
            * sum(
                q(and_(*combo))
                for combo in combinations(terms, order)
            )
        )

    partial_sum = 0.

    for r in range(1, len(terms) + 1):
        latest = q_contribution(order=r)

        partial_sum += latest

        if r == computational_cache.truncation_order:
            break

        if is_within_truncation_tolerance(latest, partial_sum, computational_cache.truncation_tolerance):
            break

    return partial_sum


def uncached_expression_intensity(expression: Expression, flattened_index: int,
                                  computational_cache: ComputationalCache) -> float:
    """
    Instantaneous failure intensity for a general Boolean expression (a disjunction (OR) of terms).

    From `MATHS.md`, for a gate `T` represented as a disjunction of `N` minimal cut sets,
        T = C_1 + C_2 + ... + C_N,
    the failure intensity `ω[T]` of the top gate is given by
        ω[T] = ω^1[T] − ω^2[T],
    where
        ω^1[T] =   ∑{1≤i≤N} ω[C_i]
                 − ∑{1≤i<j≤N} ω[gcd(C_i,C_j)] q[C_i C_j ÷ gcd(C_i,C_j)]
                 + ... ,
        ω^2[T] =   ∑{1≤i≤N} ω^†[C_i]
                 − ∑{1≤i<j≤N} ω^†[C_i,C_j]
                 + ... ,
        ω^†[C_i,C_j,...]
               =   ∑{1≤a≤N} ω[gcd(C_i,C_j,...) ÷ (C_a)] q[(C_a) (C_i C_j ... ÷ gcd(C_i,C_j,...))]
                 − ∑{1≤a<b≤N} ω[gcd(C_i,C_j,...) ÷ (C_a C_b)] q[(C_a C_b) (C_i C_j ... ÷ gcd(C_i,C_j,...))]
                 + ... .
    Successive upper, lower, upper, ... bounds may be obtained by computing
        (ω^1 truncated at 1st-order),
        (ω^1 truncated at 2nd-order) − (ω^2 truncated at 1st-order with ω^† truncated at 1st-order),
        (ω^1 truncated at 3rd-order) − (ω^2 truncated at 2nd-order with ω^† truncated at 2nd-order),
        (ω^1 truncated at 4th-order) − (ω^2 truncated at 3rd-order with ω^† truncated at 3rd-order),
        etc.
    To avoid unnecessary recomputation, we implement this by computing the successive contributions
        (ω^1 1st-order contribution),
        (ω^1 2nd-order contribution) − (ω^2 1st-order contribution with ω^† truncated at 1st-order),
        (ω^1 3rd-order contribution) − (ω^2 (1st)-order contribution's ω^† 2nd-order contribution
                                     − (ω^2 2nd-order contribution with ω^† truncated at 2nd-order),
        (ω^1 4th-order contribution) − (ω^2 (1st,2nd)-order contributions' ω^† 3rd-order contribution
                                     − (ω^2 3rd-order contribution with ω^† truncated at 3rd-order),
        etc.
    Thus, we truncate if the truncation order is reached, or after the latest contribution
        (ω^1 rth-order contribution) − (ω^2 (1,...,r−2)th-order contributions' ω^† (r−1)th-order contribution)
                                     − (ω^2 (r−1)th-order contribution with ω^† truncated at (r−1)th-order)
    divided by the partial sum falls below the truncation tolerance.
    """
    terms = expression.terms

    gcd = Term.gcd
    and_ = Term.conjunction
    combinations = computational_cache.term_combinations

    def q(term: Term) -> float:
        return computational_cache.term_probability(term, flattened_index)

    def omega(term: Term) -> float:
        return computational_cache.term_intensity(term, flattened_index)

    def omega_1_contribution(order: int) -> float:
        return (
            (-1) ** (order - 1)
            * sum(
                omega(combo_gcd) * q(and_(*combo) / combo_gcd)
                for combo in combinations(terms, order)
                if not (combo_gcd := gcd(*combo)).is_vacuous()  # skip q computation if omega is zero
            )
        )

    def omega_2_contribution(order: int, omega_dagger_orders: Iterable[int]) -> float:
        return (
            (-1) ** (order - 1)
            * sum(
                omega_dagger_contributions(combo, omega_dagger_orders)
                for combo in combinations(terms, order)
            )
        )

    def omega_dagger_contributions(combo: tuple[Term, ...], orders: Iterable[int]) -> float:
        return sum(
            omega_dagger_contribution(combo, order)
            for order in orders
        )

    def omega_dagger_contribution(combo: tuple[Term, ...], order: int) -> float:
        return (
            (-1) ** (order - 1)
            * sum(
                omega(combo_gcd_divided_by_failed) * q(and_(*failed, and_(*combo) / combo_gcd))
                for failed in combinations(terms, order)
                if not (combo_gcd := gcd(*combo)).is_vacuous()  # skip q computation if omega is zero
                if not (combo_gcd_divided_by_failed := combo_gcd / and_(*failed)).is_vacuous()  # ditto
            )
        )

    partial_sum = 0.

    for r in range(1, len(terms) + 1):
        latest = (
            omega_1_contribution(order=r)
            - sum(
                omega_2_contribution(order=s, omega_dagger_orders=[r-1])
                for s in range(1, r-1)
            )
            - omega_2_contribution(order=r-1, omega_dagger_orders=range(1, r))
        )

        partial_sum += latest

        if r == computational_cache.truncation_order:
            break

        if is_within_truncation_tolerance(latest, partial_sum, computational_cache.truncation_tolerance):
            break

    return partial_sum


def is_within_truncation_tolerance(latest: float, partial_sum: float, tolerance: float) -> bool:
    """
    Predicate for early termination (truncation) of disjunction probability and intensity computations.
    """
    return math.isnan(latest) or latest == 0 or abs(latest) < abs(partial_sum) * tolerance
