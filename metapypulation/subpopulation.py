"""
A module containing the subpopulation class.
"""

from collections.abc import Iterator, MutableSet
import numpy as np
import random
from typing import List, Tuple

from .individual import Individual


class Subpopulation():
    """
    The base class for a subpopulation in the metapopulation.
    
    Attributes:
        id (int): Unique id of the subpopulation.
        population (SetOfIndividuals): Set containing all the individuals in the subpopulation
        outgoing_migrants (SetOfIndividuals): Set containing individuals that are being prepared for emigration. Empty outside of the migration step.
        incoming_migrants (SetOfIndividuals): Set containind individuals that were received through immigration. Empty outside of the migration step.
        type_of_interaction (str): The type of interaction to implement between individuals for cultural changes. Currently accepts only "axelrod_interaction".
    """
    def __init__(self, id: int, type_of_interaction: str):
        """
        Create a new subpopulation.

        Args:
            id (int): Identifier of the population.
            type_of_interaction (str): The type of interaction to implement between individuals for cultural changes. Currently accepts only "axelrod_interaction".
        """
        self.id = id
        self.population = SetOfIndividuals(self)
        self.outgoing_migrants = SetOfIndividuals(self) # CONSIDER removing since migration works with incoming_migrants
        self.incoming_migrants = SetOfIndividuals(self)
        self.type_of_interaction = type_of_interaction
        
        
    def get_population_size(self) -> int:
        """
        Returns the current subpopulation size.

        Returns:
            int: Current subpopulation size.
        """
        return len(self.population)
    
    
    def get_current_number_of_migrants(self) -> int:
        """
        Returns the current number of incoming immigrants during. Only returns a non-zero number during the migration step.

        Returns:
            int: Current number of immigrants.
        """
        return len(self.incoming_migrants)
    
        
    def list_migrants(self, migration_rate: float) -> None:
        """Create a list of migrants that will be sent out of the subpopulation.

        Args:
            migration_rate (float): The migration rate is defined as the expected percentage of population that will migrate at each generation.

        Returns:
            List[Individual]: A list of individuals from the subpopulation.
        """
        # CONSIDER removing this function if self.outgoing_migrants falls out of use.
        size = self.get_population_size()
        number_of_migrants = np.random.binomial(size, migration_rate)
        if number_of_migrants > 0:
            individuals_to_remove = self.population.sample_and_remove(number_of_migrants)
            for individual in individuals_to_remove:
                self.outgoing_migrants.add(individual)   
                
    
    def receive_migrants(self, giving_subpopulation: "Subpopulation", migration_rate: float) -> None:
        """Populate the list of incoming migrants with individuals coming from a giving_subpopulation.

        Args:
            giving_subpopulation (Subpopulation): Subpopulation from which individuals are migrating.
            migration_rate (float): Percentage of the giving subpopulation that will migrate at each generation into the current subpopulation.

        Returns:
            List[Individual]: A list of individuals from the giving subpopulation.
        """
        population_size = giving_subpopulation.get_population_size()
        number_of_migrants = np.random.binomial(population_size, migration_rate)
        if number_of_migrants > 0:
            individuals_to_remove = giving_subpopulation.population.sample_and_remove(number_of_migrants)
            for individual in individuals_to_remove:
                self.incoming_migrants.add(individual)
            
                
    def incorporate_migrants_in_population(self) -> None:
        """
        Merges incoming migrants into the local population.
        """
        for individual in self.incoming_migrants:
            self.population.add(individual)
        
        self.incoming_migrants.empty_set()
        
        
    def add_individual(self, individual: "Individual") -> None:
        """
        Adds an individual to the subpopulation. This function does not remove the individual from somewhere else (in case of passages from list to list).

        Args:
            individual (Individual): individual to be added to the subpopulation.
        """
        self.population.add(individual)
        

    def create_interaction(self) -> None:
        """
        Samples two individuals at random in the subpopulation and makes them interact.
        """
        index_focus, index_interacting = np.random.choice(range(self.get_population_size()), 2)
        focus_individual = self.population.individuals[index_focus]
        interacting_individual = self.population.individuals[index_interacting]
        focus_individual.interact(interacting_individual, self.type_of_interaction)
    

    def get_traits_sets(self) -> np.ndarray:
        """
        This function returns all the feature sets found in a subpopulation in an array.

        Returns:
            np.ndarray: All the current sets of features in the subpopulation.
        """
        number_of_features = self.population.individuals[0].number_of_features
        traits = np.zeros((self.get_population_size(), number_of_features))
        i = 0
        for individual in self.population:
            traits[i] = (individual.features)
            i += 1

        return traits

    
    def count_traits_sets(self) -> int:
        """
        This function counts the total of unique sets of traits in the subpopulation. For example,
        [0, 1, 2, 3, 4] is a set different from [1, 1, 2, 3, 4], which is different from [5, 4, 3, 2, 1], etc.    
        
        Returns:
            int: The current number of different sets of traits in the subpopulation.
        """
        traits = self.get_traits_sets()    
        
        uniques = np.unique(traits, axis = 0)
        
        return len(uniques)   


    def is_trait_in_subpopulation(self, trait: int, feature: int = None) -> bool:
        """
        This function checks whether a given trait at a given feature is in the population.

        Args:
            trait (int): the int referring to the trait that needs to be checked against
            feature (Optional, int): the feature that needs to be checked (index from 0 to N_features-1). If None, it checks for the trait in any feature. Default is None.
        Returns:
            bool: True if the trait is found in the subpopulation.
        """ 
        traits = self.get_traits_sets()

        if feature is None:
            feature_is_found = (trait in traits)

        else: 
            feature_is_found = (trait in traits[:,feature])

        return feature_is_found
            
        
    def shannon_diversity(self) -> float:
        """
        Calculate the Shannon diversity index in the subpopulation.
        
        Returns:
            float: The current Shannon diversity index in the subpopulation.
        """
        traits = self.get_traits_sets()    
        uniques, counts = np.unique(traits, axis = 0, return_counts=True)
        frequencies = counts / self.get_population_size()
        shannon_index = -np.sum(frequencies*np.log(frequencies))
        
        return shannon_index
        
    
    def simpson_diversity(self) -> float:
        """
        Calculate the Simpson diversity index of the subpopulation.

        Returns:
            float: The Simpson diversity index of the subpopulation.
        """
        traits = self.get_traits_sets()    
        uniques, counts = np.unique(traits, axis = 0, return_counts=True)
        frequencies = counts / self.get_population_size()
        simpson_diversity_index = np.sum(frequencies*frequencies)
        
        return simpson_diversity_index

    
    def gini_diversity(self) -> float:
        """
        Calculate the Gini-Simpson diversity index of the subpopulation. This is equal to 1 - Simpson_index

        Returns:
            float: The Gini-Simpson diversity index of the subpopulation.
        """
        traits = self.get_traits_sets()    
        uniques, counts = np.unique(traits, axis = 0, return_counts=True)
        frequencies = counts / self.get_population_size()
        gini_diversity_index = 1 - np.sum(frequencies*frequencies)
        
        return gini_diversity_index

    
    def count_deme_origin_id(self, total_number_of_subpopulations: int) -> List[int]:
        """
        Count how many individuals originally from each deme are found in this deme. It is generally invoked from Metapopulation to get a summary. 

        Args:
            total_number_of_subpopulations: number of subpopulations in the whole metapopulation.

        Returns:
            List[int]: list containing a count of individuals for each subpopulation present.
        """
        counts = [0]*total_number_of_subpopulations
        for individual in self.population:
            counts[individual.original_deme_id] += 1

        return counts

      
class IndividualsIterator(object):
    """
    An iterator object ot iterate over the SetOfSubpopulations class.
    """
    def __init__(self, individuals):
        self.idx = 0
        self.data = individuals
    def __iter__(self):
        return self
    def __next__(self):
        self.idx += 1
        try:
            return self.data[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration


class SetOfIndividuals(MutableSet):
    """
    A class inheriting from MutableSet to act as container of Individual objects. Methods are standard for a MutableSet.

    """
    def __init__(self, deme: Subpopulation):
        self.individuals = []
        self.deme = deme.id
        self.index = len(self.individuals)
        
    def __contains__(self, individual: Individual) -> bool:
        """Checks if an agent is in the SetOfIndividuals.

        Args:
            individual (Individual): An Individual in the set.

        Returns:
            bool: Whether the individual exists in the set.
        """
        return individual in self.individuals
    
    def __iter__(self) -> Iterator[Individual]:
        """Provides an iterator for the SetOfIndividuals.

        Returns:
            Interator[Individual]: Iterator for the set.
        """
        return IndividualsIterator(self.individuals)#.individuals.keys()
    
    def __len__(self) -> int:
        """Returns the length of the SetOfIndividuals.

        Returns:
            int: Number of individuals in the Set.
        """
        return len(self.individuals)
    
    def __getitem__(self, item: int | slice) -> Individual:
        """
        Retrieve an agent or a slice of agents from the SetOfIndividuals. Taken from mesa.agent.

        Args:
            item (int | slice): The index or slice for selecting agents.

        Returns:
            Agent | list[Agent]: The selected agent or list of agents based on the index or slice provided.
        """
        return list(self.individuals)[item]
    
    def add(self, individual: Individual):
        """Adds an Individual to the SetOfIndividuals.

        Args:
            individual (Individual): Individual to add to the set.
        """
        self.individuals.append(individual)
        
    def discard(self, individual: Individual):
        """Eliminates an individual from the set (and from the population). 

        Args:
            individual (Individual): Individual to be discarded.
        """
        del self.individuals[individual]
        
    def empty_set(self) -> None:
        """
        Empty the Set.
        """
        self.individuals = []
        # for individual in self.individuals:
        #     self.discard(individual)

    def shuffle(self) -> None:
        """
        Shuffle the Set.
        """
        random.shuffle(self.individuals)
        
    def sample_and_remove(self, number_of_individuals: int) -> List[Individual]:
        """
        Sample an individual, remove it from the Set and return it in a list.

        Args:
            number_of_individuals (int): Number of individuals to sample randomly. 

        Returns:
            List[Individual]: List of all the individuals that have been sampled from the population.
        """
        self.shuffle()
        
        list_of_individuals = []
        for i in range(number_of_individuals):
            individual = self.individuals.pop()
            list_of_individuals.append(individual)
            
        return list_of_individuals
        
        