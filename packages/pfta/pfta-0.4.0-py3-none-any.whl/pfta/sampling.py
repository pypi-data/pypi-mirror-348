"""
# Public Fault Tree Analyser: sampling.py

Distribution sampling (i.e. pseudo-random number generation).

**Copyright 2025 Conway.**
Licensed under the GNU General Public License v3.0 (GPL-3.0-only).
This is free software with NO WARRANTY etc. etc., see LICENSE.
"""

import math
import random

from pfta.common import natural_repr
from pfta.woe import FaultTreeTextException


class InvalidDistributionParameterException(FaultTreeTextException):
    pass


class Distribution:
    line_number: int

    def __init__(self, line_number: int):
        self.line_number = line_number

    def __repr__(self):
        return natural_repr(self, omitted_attributes=('line_number',))

    def generate_samples(self, count: int) -> list[float]:
        raise NotImplementedError


class DegenerateDistribution(Distribution):
    value: float

    def __init__(self, value: float, line_number: int):
        self.value = value
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        return [self.value for _ in range(count)]


class BetaDistribution(Distribution):
    alpha: float
    beta: float

    def __init__(self, alpha: float, beta: float, line_number: int):
        if not math.isfinite(alpha) or alpha <= 0:
            raise InvalidDistributionParameterException(
                line_number,
                f'beta distribution parameter `alpha={alpha}` not finite positive',
            )

        if not math.isfinite(beta) or beta <= 0:
            raise InvalidDistributionParameterException(
                line_number,
                f'beta distribution parameter `beta={beta}` not finite positive',
            )

        self.alpha = alpha
        self.beta = beta
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        alpha = self.alpha
        beta = self.beta

        return [random.betavariate(alpha, beta) for _ in range(count)]


class GammaDistribution(Distribution):
    alpha: float
    lambda_: float

    def __init__(self, alpha: float, lambda_: float, line_number: int):
        if not math.isfinite(alpha) or alpha <= 0:
            raise InvalidDistributionParameterException(
                line_number,
                f'gamma distribution parameter `alpha={alpha}` not finite positive',
            )

        if not math.isfinite(lambda_) or lambda_ <= 0:
            raise InvalidDistributionParameterException(
                line_number,
                f'gamma distribution parameter `lambda={lambda_}` not finite positive',
            )

        self.alpha = alpha
        self.lambda_ = lambda_
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        alpha = self.alpha
        lambda_ = self.lambda_

        return [random.gammavariate(alpha, beta=1 / lambda_) for _ in range(count)]


class LogNormalDistribution(Distribution):
    mu: float
    sigma: float

    def __init__(self, mu: float, sigma: float, line_number: int):
        self.mu = mu
        self.sigma = sigma
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        mu = self.mu
        sigma = self.sigma

        return [random.lognormvariate(mu, sigma) for _ in range(count)]


class LogUniformDistribution(Distribution):
    lower: float
    upper: float

    def __init__(self, lower: float, upper: float, line_number: int):
        if lower <= 0:
            raise InvalidDistributionParameterException(
                line_number,
                f'loguniform distribution parameter `lower={lower}` not positive',
            )

        if upper <= 0:
            raise InvalidDistributionParameterException(
                line_number,
                f'loguniform distribution parameter `upper={upper}` not positive',
            )

        self.lower = lower
        self.upper = upper
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        a = self.lower
        b = self.upper

        return [math.exp(random.uniform(math.log(a), math.log(b))) for _ in range(count)]


class NormalDistribution(Distribution):
    mu: float
    sigma: float

    def __init__(self, mu: float, sigma: float, line_number: int):
        self.mu = mu
        self.sigma = sigma
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        mu = self.mu
        sigma = self.sigma

        return [random.normalvariate(mu, sigma) for _ in range(count)]


class TriangularDistribution(Distribution):
    lower: float
    upper: float
    mode: float

    def __init__(self, lower: float, upper: float, mode: float, line_number: int):
        self.lower = lower
        self.upper = upper
        self.mode = mode
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        low = self.lower
        high = self.upper
        mode = self.mode

        return [random.triangular(low, high, mode) for _ in range(count)]


class UniformDistribution(Distribution):
    lower: float
    upper: float

    def __init__(self, lower: float, upper: float, line_number: int):
        self.lower = lower
        self.upper = upper
        super().__init__(line_number)

    def generate_samples(self, count: int) -> list[float]:
        a = self.lower
        b = self.upper

        return [random.uniform(a, b) for _ in range(count)]
