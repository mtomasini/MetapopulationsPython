"""
A module containing the class Metapopulation, which determines the topology of the metapopulation 
as well as the migration rates between populations.
"""

from collections.abc import Set, Iterator
from itertools import permutations
import numpy as np
import pandas as pd
from typing import List

from .individual import Individual
from .subpopulation import Subpopulation, SetOfIndividuals

class Metapopulation():
    """
    The base class for a metapopulation containing subpopulations.
    
    Attributes:
        number_of_subpopulations (int): how many subpopulations compose the metapopulation.
        subpopulations (SetOfSubpopulations): the list of Subpopulation objects in the metapopulation.
        type_of_interaction (str): The type of interaction to implement between individuals for cultural changes. Currently accepts only "axelrod_interaction".
        migration_matrix (np.ndarray): A matrix determining migration rates between subpopulations.
        carrying_capacities (List[int] | int): A list of carrying capacities (one for each subpopulation) or an integer (same carrying capacity for each subpopulation).
        number_of_features (int): Total number of cultural features per individual.
        number_of_traits (int, optional): Number of different possible traits for each cultural feature.
        mutation_rate (float, optional): Probability of a mutation to occur.
        min_trait (int, optional): Minimum value for a trait in each feature. 
        max_trait (int, optional): Maximum value for a trait in each feature. 
    """
    def __init__(self, number_of_subpopulations: int, 
                 type_of_interaction: str,
                 migration_matrix: np.ndarray = None, 
                 carrying_capacities: List[int] | int = 100,
                 number_of_features: int = 5,
                 number_of_traits: int = 10,
                 mutation_rate: float = 0.0,
                 min_trait: int = 1,
                 max_trait: int = 10
                 ):
        """Creates an empty metapopulation.

        Args:
            number_of_subpopulations (int): The total number of subpopulations to create. 
            type_of_interaction (str): A string that determines which interaction function to call on. Possibilities are "axelrod_interaction".
            migration_matrix (np.ndarray, optional): A matrix determining migration rates between subpopulations. Defaults to None.
            carrying_capacities (List[int] | int, optional): Either a list of carrying capacities (of which the `len()` is the same as `number_of_subpopulations`) or single integer determining the same carrying capacity for all subpopulations. Defaults to 100.
            number_of_features (int, optional): Total number of cultural features per individual. Defaults to 5.
            number_of_traits (int, optional): Number of different possible traits for each cultural feature. Defaults to 10.
            mutation_rate (float, optional): Probability of a mutation to occur. Defaults to 0.0.
            min_trait (int, optional): Minimum value for a trait in each feature. Defaults to 1.
            max_trait (int, optional): Maximum value for a trait in each feature. Deafults to 10.
        """
        self.number_of_subpopulations = number_of_subpopulations
        self.subpopulations = SetOfSubpopulations(number_of_subpopulations, type_of_interaction)
        self.type_of_interaction = type_of_interaction
        self.migration_matrix = migration_matrix
        self.carrying_capacities = carrying_capacities
        self.number_of_features = number_of_features
        self.number_of_traits = number_of_traits
        self.mutation_rate = mutation_rate
        self.min_trait = min_trait
        self.max_trait = max_trait
        
        
    def populate(self) -> None:
        """Populate all (empty) subpopulations within the Metapopulation class. 
        
        The populate step can take either a list of carrying capacities, a different number per each subpopulation,
        or one single carrying capacity that will determine the same number of individuals for each subpopulation.
        """
        match self.carrying_capacities:
            case list():
                assert self.number_of_subpopulations == len(self.carrying_capacities)
                for subpopulation in self.subpopulations:
                    for i in range(self.carrying_capacities[subpopulation.id]):
                        derived_number_of_traits = self.max_trait - self.min_trait + 1 # e.g. if smaller trait is 1 and largest is 10, there are 10 traits: 10 - 1 + 1 
                        set_of_features = np.random.randint(low = self.min_trait, high = self.max_trait + 1, size = self.number_of_features)
                        new_individual = Individual(i, subpopulation.id, self.number_of_features, derived_number_of_traits, self.mutation_rate, set_of_features)
                        subpopulation.add_individual(new_individual)
            case int():
                for subpopulation in self.subpopulations:
                    for i in range(self.carrying_capacities):
                        derived_number_of_traits = self.max_trait - self.min_trait + 1 # e.g. if smaller trait is 1 and largest is 10, there are 10 traits: 10 - 1 + 1 
                        set_of_features = np.random.randint(low = self.min_trait, high = self.max_trait + 1, size = self.number_of_features)
                        new_individual = Individual(i, subpopulation.id, self.number_of_features, derived_number_of_traits, self.mutation_rate, set_of_features)
                        subpopulation.add_individual(new_individual)
                
        
    def migrate(self) -> None:
        """A function that causes the migration step for a subpopulation. 
        When called, each subpopulation finds to what subpopulations it needs to send individuals (based on
        the migration matrix supplied), and it calls upon the `subpopulation.receive_migrants()` function of 
        the destinations.
        
        After each subpopulation has received the migrants, the function `subpopulation.incorporate_migrants_in_population()`
        is called for each subpopulation. This merges the incoming migrants with the already existing population.
        """
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
            
            
    def get_metapopulation_size(self) -> int:
        """
        Calculates the full size of the metapopulation. In the absence of population reduction strategies, this is always
        equal to the sum of all the carrying capacities.

        Returns:
            int: the number of individuals in the whole metapopulation.
        """
        population_size = 0
        for subpopulation in self.subpopulations:
            population_size += subpopulation.get_population_size()
    
        return population_size
    
    
    def make_interact(self) -> None:
        """
        Make one interaction in each subpopulation.
        """
        for subpopulation in self.subpopulations:
            subpopulation.create_interaction()
            
        
    def shannon_diversity_per_subpopulation(self) -> List[float]:
        """
        Calculates Shannon diversity index in each subpopulation.

        Returns:
            List[float]: list with the Shannon diversity index per subpopulation.
        """
        subpopulation_shannons = []
        for subpopulation in self.subpopulations:
            subpopulation_shannons.append(subpopulation.shannon_diversity())
            
        return subpopulation_shannons
    
    
    def traits_sets_per_subpopulation(self) -> List[int]:
        """
        Calculates number of unique sets of traits per each subpopulation.

        Returns:
            List[int]: list with the number of unique sets per subpopulation.
        """
        subpopulation_counts = []
        for subpopulation in self.subpopulations:
            subpopulation_counts.append(subpopulation.count_traits_sets())
            
        return subpopulation_counts
    
    
    def metapopulation_shannon_diversity(self) -> float:
        """
        Calculates Shannon diversity trait over the whole metapopulation.

        Returns:
            float: Shannon diversity index of the metapopulation.
        """
        number_of_features = self.number_of_features
        traits = np.zeros((self.get_metapopulation_size(), number_of_features))
        i = 0
        for subpopulation in self.subpopulations:
            for individual in subpopulation.population:
                traits[i] = (individual.features)
                i += 1
            
        uniques, counts = np.unique(traits, axis = 0, return_counts = True)

        frequencies = counts / self.get_metapopulation_size()
        shannon_diversity_index = -np.sum(frequencies*np.log(frequencies))
        
        return shannon_diversity_index
        
    
    def metapopulation_test_sets(self) -> int:
        """Calculates number of unique sets of traits in the whole metapopulation.

        Returns:
            int: number of unique sets in the metapopulation.
        """
        number_of_features = self.number_of_features
        traits = np.zeros((self.get_metapopulation_size(), number_of_features))
        i = 0
        for subpopulation in self.subpopulations:
            for individual in subpopulation.population:
                traits[i] = (individual.features)
                i += 1
            
        uniques = np.unique(traits, axis = 0)
        
        return len(uniques) 

    def metapopulation_simpson(self) -> float:
        """
        Calculates Simpson diversity index over the whole metapopulation.

        Returns:
            float: Simpson diversity index of the metapopulation.
        """
        number_of_features = self.number_of_features
        traits = np.zeros((self.get_metapopulation_size(), number_of_features))
        i = 0
        for subpopulation in self.subpopulations:
            for individual in subpopulation.population:
                traits[i] = (individual.features)
                i += 1
            
        uniques, counts = np.unique(traits, axis = 0, return_counts = True)

        frequencies = counts / self.get_metapopulation_size()
        simpson_diversity_index = np.sum(frequencies*frequencies)
        
        return simpson_diversity_index


    def count_origin_id_spread(self) -> np.ndarray:
        """
        Counts the spread of individuals from deme of origin by counting how many individuals from each deme are in each deme.

        Returns:
            np.ndarray: NxN matrix where N is the number of subpopulations. Rows are local subpopulations, columns are the original deme id.
        """

        counts = []

        for subpopulation in self.subpopulations:
            local_spread = subpopulation.count_deme_origin_id(self.number_of_subpopulations)
            counts.append(local_spread)
        
        return np.array(counts)

        
class SubpopulationIterator(object):
    """
    An iterator object ot iterate over the SetOfSubpopulations class.
    """
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
    """
    A class inheriting from Set to act as container of Subpopulation objects. Methods are standard for a Set.

    """
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
            int: number of subpopulations in the set.
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