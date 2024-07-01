"""
A module containing the individual class.
"""

import numpy as np

class Individual():
    def __init__(self, id: int, original_deme_id: int, number_of_features: int, number_of_traits: int):
        self.id = id
        self.original_deme_id = original_deme_id
        
        # number of traits is +1 as the argument high is exclusive
        self.features = np.random.randint(low = 1, high = number_of_traits + 1, size = number_of_features)