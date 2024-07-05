"""
A module containing the individual class.
"""

import numpy as np
from typing import Callable

class Individual():
    def __init__(self, id: int, original_deme_id: int, number_of_features: int, number_of_traits: int):
        self.id = id
        self.original_deme_id = original_deme_id
        self.number_of_features = number_of_features
        self.number_of_traits = number_of_traits
        
        # number of traits is +1 as the argument high is exclusive
        self.features = np.random.randint(low = 1, high = number_of_traits + 1, size = number_of_features)
        self.number_of_changes = 0
        
    
    def axelrod_interaction(self, interacting_individual: "Individual") -> None:
        probability_of_interaction = 1 - np.count_nonzero(self.features - interacting_individual.features)/self.number_of_features
        random_number = np.random.rand()
        if (random_number <= probability_of_interaction) and (probability_of_interaction < 1.0):
            index = np.random.choice(np.nonzero(self.features - interacting_individual.features)[0])
            self.features[index] = interacting_individual.features[index]
            self.number_of_changes += 1
            
            
    def interact(self, interacting_individual: "Individual", interaction_function: str) -> None:
        match interaction_function:
            case "axelrod_interaction":
                self.axelrod_interaction(interacting_individual)