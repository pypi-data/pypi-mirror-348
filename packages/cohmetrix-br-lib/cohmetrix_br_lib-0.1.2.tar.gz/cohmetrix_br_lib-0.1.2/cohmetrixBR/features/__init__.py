"""Init file.
"""
from . import (connectives, descriptive, lexical_diversity_coh,
               readability, referential_cohesion, situation_model,
               syntactic_complexity, syntactic_pattern_density,
               word_information)

FEATURES =\
    descriptive.FEATURES +\
    referential_cohesion.FEATURES +\
    lexical_diversity_coh.FEATURES +\
    connectives.FEATURES +\
    situation_model.FEATURES +\
    syntactic_complexity.FEATURES +\
    syntactic_pattern_density.FEATURES +\
    word_information.FEATURES +\
    readability.FEATURES
