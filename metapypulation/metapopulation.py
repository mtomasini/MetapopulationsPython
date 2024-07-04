"""
A module containing the class Metapopulation, which determines the topology of the metapopulation as well as the migration rates between populations.
"""

from collections.abc import Set, Iterator
import pandas as pd

from .subpopulation import Subpopulation

class Metapopulation():
    def __init__(self, number_of_subpopulations: int, migration_matrix: pd.DataFrame = None):
        self.number_of_subpopulations = number_of_subpopulations
        self.subpopulations = SetOfSubpopulations(number_of_subpopulations)
        
        
        
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
    def __init__(self, number_of_subpopulations: int):
        self.subpopulations = []
        for subpopulation in range(number_of_subpopulations):
            self.subpopulations.append(Subpopulation(id = subpopulation))
        
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