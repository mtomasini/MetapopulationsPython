"""
A module containing the class Metapopulation, which determines the topology of the metapopulation as well as the migration rates between populations.
"""

from collections.abc import Set, Iterator
from itertools import permutations
import numpy as np
import pandas as pd
from typing import List

from .individual import Individual
from .subpopulation import Subpopulation

class Metapopulation():
    def __init__(self, number_of_subpopulations: int, 
                 type_of_interaction: str,
                 migration_matrix: np.ndarray = None, 
                 carrying_capacities: List[int] | int = 100,
                 number_of_features: int = 5,
                 number_of_traits: int = 10 
                 ):
        self.number_of_subpopulations = number_of_subpopulations
        self.subpopulations = SetOfSubpopulations(number_of_subpopulations, type_of_interaction)
        self.type_of_interaction = type_of_interaction
        self.migration_matrix = migration_matrix
        self.carrying_capacities = carrying_capacities
        self.number_of_features = number_of_features
        self.number_of_traits = number_of_traits
        
        
    def populate(self):
        match self.carrying_capacities:
            case list():
                assert self.number_of_subpopulations == len(self.carrying_capacities)
                for subpopulation in self.subpopulations:
                    for i in range(self.carrying_capacities[subpopulation.id]):
                        new_individual = Individual(i, subpopulation.id, self.number_of_features, self.number_of_traits)
                        subpopulation.add_individual(new_individual)
            case int():
                for subpopulation in self.subpopulations:
                    for i in range(self.carrying_capacities):
                        new_individual = Individual(i, subpopulation.id, self.number_of_features, self.number_of_traits)
                        subpopulation.add_individual(new_individual)
                
        
    def migrate(self):
        # for each subpopulation we create a list of individuals that will migrate, based on the migration rates matrix
        for subpopulation in self.subpopulations:
            # find id of populations to which migration happens:
            migrate_to = np.nonzero(self.migration_matrix[subpopulation.id])[0]
            
            # for each non zero migration rate, find the receiving population and populate its incoming_migrants list
            for index in migrate_to:
                migration_rate = self.migration_matrix[subpopulation.id][index]
                receiving_subpopulation = self.subpopulations[index]
            
                receiving_subpopulation.receive_migrants(subpopulation, migration_rate)
        
        for subpopulation in self.subpopulations:
            subpopulation.incorporate_migrants_in_population() 
            
    
    def make_interact(self):
        for subpopulation in self.subpopulations:
            subpopulation.create_interaction()
            
            
        
        
class SubpopulationIterator(object):
    def __init__(self, subpopulations):
        self.idx = 0
        self.data = subpopulations
    def __iter__(self):
        return self
    def __next__(self):
        self.idx += 1
        try:
            return self.data[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration


class SetOfSubpopulations(Set):
    def __init__(self, number_of_subpopulations: int, type_of_interaction: str):
        self.subpopulations = []
        for subpopulation in range(number_of_subpopulations):
            self.subpopulations.append(Subpopulation(id = subpopulation, type_of_interaction = type_of_interaction))
        
    def __contains__(self, subpopulation: Subpopulation) -> bool:
        """Checks if an agent is in the SetOfIndividuals.

        Args:
            individual (Individual): an Individual in the set.

        Returns:
            bool: whether the individual exists in the set.
        """
        return subpopulation in self.subpopulations
    
    def __iter__(self) -> Iterator[Subpopulation]:
        """Provides an iterator for the SetOfIndividuals.

        Returns:
            Interator[Individual]: iterator for the set.
        """
        return SubpopulationIterator(self.subpopulations)
    
    def __len__(self) -> int:
        """Returns the length of the SetOfIndividuals.

        Returns:
            int: _description_
        """
        return len(self.subpopulations)
    
    def __getitem__(self, item: int | slice) -> Subpopulation:
        """
        Retrieve an agent or a slice of agents from the SetOfIndividuals. Took from mesa.agent.

        Args:
            item (int | slice): The index or slice for selecting agents.

        Returns:
            Agent | list[Agent]: The selected agent or list of agents based on the index or slice provided.
        """
        return list(self.subpopulations)[item]