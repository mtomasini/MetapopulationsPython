"""
A module containing the individual class.
"""

import numpy as np
from typing import Callable

class Individual():
    """
    Base class for an individual in the metapopulation.
    
    Attributes:
        id (int): The identifier for the individual (unique within the subpopulation).
        original_deme_id (int): Identifier of the deme where the individual originated.
        number_of_features (int): Number of cultural features of the individual.
        number_of_traits (int): Number of traits per feature of the individual.
        features (List[int]): List of features of the individual.
        number_of_changes (int): The number of times this individual has changed set of features following an interaction.
    """
    def __init__(self, id: int, original_deme_id: int, number_of_features: int, number_of_traits: int):
        """
        Create a new individual with a random set of features.

        Args:
            id (int): The identifier for the individual (unique within the subpopulation).
            original_deme_id (int): Identifier of the deme where the individual originated.
            number_of_features (int): Number of cultural features of the individual.
            number_of_traits (int): Number of traits per feature of the individual.
        """
        self.id = id
        self.original_deme_id = original_deme_id
        self.number_of_features = number_of_features
        self.number_of_traits = number_of_traits
        
        # number of traits is +1 as the argument high is exclusive
        self.features = np.random.randint(low = 1, high = number_of_traits + 1, size = number_of_features)
        self.number_of_changes = 0
        
    
    def axelrod_interaction(self, interacting_individual: "Individual") -> None:
        """
        Interaction following the Axelrod model of culture dissemination.

        Args:
            interacting_individual (Individual): Individual with which the self individual interacts. Currently accepts only "axelrod_interaction".
        """
        probability_of_interaction = 1 - np.count_nonzero(self.features - interacting_individual.features)/self.number_of_features
        random_number = np.random.rand()
        if (random_number <= probability_of_interaction) and (probability_of_interaction < 1.0):
            index = np.random.choice(np.nonzero(self.features - interacting_individual.features)[0])
            self.features[index] = interacting_individual.features[index]
            self.number_of_changes += 1
            
            
    def interact(self, interacting_individual: "Individual", interaction_function: str) -> None:
        """
        Wrapper for interactions, it allows to pass any interaction that is coded for.

        Args:
            interacting_individual (Individual): Individual with which the self individual interacts.
            interaction_function (str): The type of interaction that decides the outcome of the interaction. Current options are only "axelrod_interaction".
        """
        match interaction_function:
            case "axelrod_interaction":
                self.axelrod_interaction(interacting_individual)