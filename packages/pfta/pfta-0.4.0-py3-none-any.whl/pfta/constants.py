"""
# Public Fault Tree Analyser: constants.py

Shared constants.

**Copyright 2025 Conway.**
Licensed under the GNU General Public License v3.0 (GPL-3.0-only).
This is free software with NO WARRANTY etc. etc., see LICENSE.
"""

import enum
import re

from pfta.common import natural_join, natural_join_backticks
from pfta.sampling import (
    BetaDistribution, GammaDistribution, LogNormalDistribution, LogUniformDistribution,
    NormalDistribution, TriangularDistribution, UniformDistribution,
)


class LineType(enum.Enum):
    BLANK = 0
    COMMENT = 1
    OBJECT = 2
    PROPERTY = 3


class EventAppearance(enum.Enum):
    BASIC = 0
    UNDEVELOPED = 1
    HOUSE = 2


class GateType(enum.Enum):
    NULL = 0
    OR = 1
    AND = 2
    VOTE = 3


class ModelType(enum.Enum):
    FIXED = 0
    CONSTANT_RATE = 1
    TRUE = 2
    FALSE = 3


class SymbolType(enum.Enum):
    NULL_GATE = 0
    OR_GATE = 1
    AND_GATE = 2
    VOTE_GATE = 3
    PAGED_GATE = 4
    BASIC_EVENT = 5
    UNDEVELOPED_EVENT = 6
    HOUSE_EVENT = 7


LINE_EXPLAINER = '\n'.join([
    'A line must have one of the following forms:',
    '    <class>: <identifier>  (an object declaration)',
    '    - <key>: <value>       (a property setting)',
    '    # <comment>            (a comment)',
    '    <blank line>           (used before the next declaration)',
])

VALID_CLASSES = ('Model', 'Event', 'Gate')
CLASS_EXPLAINER = f'An object must have class {natural_join_backticks(VALID_CLASSES, "or")}.'

VALID_ID_REGEX = re.compile(r'[a-z0-9_-]+', flags=re.IGNORECASE)
ID_EXPLAINER = 'An identifier must consist only of ASCII letters, underscores, and hyphens.'

BOOLEAN_FROM_STRING = {
    'True': True,
    'False': False,
}
IS_PAGED_EXPLAINER = (
    f'Boolean property must be {natural_join_backticks(tuple(BOOLEAN_FROM_STRING), "or")} (case-sensitive).'
)

EVENT_APPEARANCE_FROM_STRING = {
    'Basic': EventAppearance.BASIC,
    'Undeveloped': EventAppearance.UNDEVELOPED,
    'House': EventAppearance.HOUSE,
}
EVENT_APPEARANCE_EXPLAINER = (
    f'Event appearance must be {natural_join_backticks(tuple(EVENT_APPEARANCE_FROM_STRING), "or")} (case-sensitive).'
)

GATE_TYPE_EXPLAINER = (
    f'Gate type must be `NULL`, `OR`, `AND`, or of the form `VOTE(<integer>)` (case-sensitive).'
)

MODEL_TYPE_FROM_STRING = {
    'Fixed': ModelType.FIXED,
    'ConstantRate': ModelType.CONSTANT_RATE,
    'True': ModelType.TRUE,
    'False': ModelType.FALSE,
}
VALID_KEY_COMBOS_FROM_MODEL_TYPE = {
    ModelType.FIXED: (
        ('probability', 'intensity'),
    ),
    ModelType.CONSTANT_RATE: (
        ('failure_rate', 'repair_rate'),
        ('failure_rate', 'mean_repair_time'),
        ('mean_failure_time', 'repair_rate'),
        ('mean_failure_time', 'mean_repair_time'),
    ),
    ModelType.TRUE: (
        (),
    ),
    ModelType.FALSE: (
        (),
    ),
}
VALID_MODEL_TYPES = tuple(MODEL_TYPE_FROM_STRING.keys())
VALID_MODEL_KEYS = tuple({
    key: None  # dict to remove duplicates but preserve order
    for combos in VALID_KEY_COMBOS_FROM_MODEL_TYPE.values()
    for combo in combos
    for key in combo
})
MODEL_TYPE_EXPLAINER = f'Recognised model types are {natural_join_backticks(VALID_MODEL_TYPES)}'

VALID_KEYS_FROM_CLASS = {
    'FaultTree': (
        'times', 'time_unit', 'seed', 'sample_size', 'computational_order', 'computational_tolerance',
        'significant_figures', 'scientific_exponent',
    ),
    'Model': ('label', 'comment', 'model_type', *VALID_MODEL_KEYS),
    'Event': ('label', 'comment', 'model_type', *VALID_MODEL_KEYS, 'model', 'appearance'),
    'Gate': ('label', 'comment', 'is_paged', 'type', 'inputs'),
}
KEY_EXPLAINER_FROM_CLASS = {
    'FaultTree': f'Recognised keys are {natural_join_backticks(VALID_KEYS_FROM_CLASS["FaultTree"])}.',
    'Model': f'Recognised keys are {natural_join_backticks(VALID_KEYS_FROM_CLASS["Model"])}.',
    'Event': f'Recognised keys are {natural_join_backticks(VALID_KEYS_FROM_CLASS["Event"])}.',
    'Gate': f'Recognised keys are {natural_join_backticks(VALID_KEYS_FROM_CLASS["Gate"])}.',
}

DISTRIBUTION_CLASS_AND_PARAMETERS_FROM_NAME = {
    'beta': (BetaDistribution, ('alpha', 'beta')),
    'gamma': (GammaDistribution, ('alpha', 'lambda')),
    'lognormal': (LogNormalDistribution, ('mu', 'sigma')),
    'loguniform': (LogUniformDistribution, ('lower', 'upper')),
    'normal': (NormalDistribution, ('mu', 'sigma')),
    'triangular': (TriangularDistribution, ('lower', 'upper', 'mode')),
    'uniform': (UniformDistribution, ('lower', 'upper')),
}
DISTRIBUTION_EXPLAINER = '\n'.join([
    f'Recognised distributions are:',
    *[
        f'- {name}({natural_join([f"{parameter}=<value>" for parameter in parameters], penultimate_separator=None)})'
        for name, (_, parameters) in DISTRIBUTION_CLASS_AND_PARAMETERS_FROM_NAME.items()
    ],
    '- <value> (for a point value)',
])
