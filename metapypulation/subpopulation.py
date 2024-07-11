"""
A module containing the subpopulation class.
"""

from collections.abc import Iterator, MutableSet
import numpy as np
import random
from typing import List, Tuple

from .individual import Individual


class Subpopulation():
    def __init__(self, id: int, type_of_interaction: str):
        self.id = id
        self.population = SetOfIndividuals(self)
        self.outgoing_migrants = SetOfIndividuals(self) # CONSIDER removing since migration works with incoming_migrants
        self.incoming_migrants = SetOfIndividuals(self)
        self.type_of_interaction = type_of_interaction
        
        
    def get_population_size(self):
        return len(self.population)
    
    
    def get_current_number_of_migrants(self):
        return len(self.incoming_migrants)
    
        
    def list_migrants(self, migration_rate: float) -> None:
        """This function creates a list of migrants that will be sent out of the subpopulation.

        Args:
            migration_rate (float): the migration rate is defined as the expected percentage of population that will migrate at each generation.

        Returns:
            List[Individual]: a simple list of individuals from the subpopulation.
        """
        # CONSIDER removing this
        size = self.get_population_size()
        number_of_migrants = np.random.binomial(size, migration_rate)
        # indeces_to_migrate = random.sample(range(size), number_of_migrants)
        if number_of_migrants > 0:
            individuals_to_remove = self.population.sample_and_remove(number_of_migrants)
            for individual in individuals_to_remove:
                self.outgoing_migrants.add(individual)   
                
    
    def receive_migrants(self, giving_subpopulation: "Subpopulation", migration_rate: float) -> None:
        """This function populates the list of incoming migrants that come from a giving population.

        Args:
            migration_rate (float): the migration rate is defined as the expected percentage of population that will migrate at each generation.

        Returns:
            List[Individual]: a simple list of individuals from the subpopulation.
        """
        population_size = giving_subpopulation.get_population_size()
        number_of_migrants = np.random.binomial(population_size, migration_rate)
        if number_of_migrants > 0:
            individuals_to_remove = giving_subpopulation.population.sample_and_remove(number_of_migrants)
            for individual in individuals_to_remove:
                self.incoming_migrants.add(individual)
            
                
    def incorporate_migrants_in_population(self) -> None:
        for individual in self.incoming_migrants:
            self.population.add(individual)
        
        self.incoming_migrants.empty_set()
        
        
    def add_individual(self, individual: "Individual") -> None:
        self.population.add(individual)
        

    def create_interaction(self) -> None:
        index_focus, index_interacting = np.random.choice(range(self.get_population_size()), 2)
        focus_individual = self.population.individuals[index_focus]
        interacting_individual = self.population.individuals[index_interacting]
        focus_individual.interact(interacting_individual, self.type_of_interaction)
        
    
    def count_traits_sets(self) -> int:
        """
        This function counts the total of unique sets of traits in the subpopulation. For example,
        [0, 1, 2, 3, 4] is a set different from [1, 1, 2, 3, 4], which is different from [5, 4, 3, 2, 1], etc.    
        """
        number_of_features = self.population.individuals[0].number_of_features
        traits = np.zeros((self.get_population_size(), number_of_features))
        i = 0
        for individual in self.population:
            traits[i] = (individual.features)
            i += 1
            
        uniques = np.unique(traits, axis = 0)
        
        return len(uniques)    

        
    def shannon_diversity(self) -> float:
        """
        Shannon_diversity is measure of the richness / diversity in a subpopulation. The formula is
        H' = -sum(p_i * ln(p_i))
    
        where p_i is the frequency of each species i in the whole sample. The "species" are each trait separately,
        and the frequency is the occurrence of each trait in the population
        """
        number_of_features = self.population.individuals[0].number_of_features
        traits = np.zeros((self.get_population_size(), number_of_features))
        i = 0
        for individual in self.population:
            traits[i] = (individual.features)
            i += 1
        
        shannons = []
        # looping over all features, for each feature extract the frequency of each trait in the population
        for k in range(0, number_of_features):
            frequencies = []
            feature_traits = traits[:, k]
            unique, counts = np.unique(feature_traits, return_counts=True)
            for trait_count in counts:
                trait_frequency = trait_count / (self.get_population_size())
                frequencies.append(trait_frequency)
            
            frequencies = np.array(frequencies)
            shannon_for_trait = -np.sum(frequencies*np.log(frequencies))
            
            shannons.append(shannon_for_trait)

        shannon_index = np.mean(shannons)
        
        return shannon_index
        
      
class IndividualsIterator(object):
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
    def __init__(self, deme: Subpopulation):
        self.individuals = []
        self.deme = deme.id
        self.index = len(self.individuals)
        
    def __contains__(self, individual: Individual) -> bool:
        """Checks if an agent is in the SetOfIndividuals.

        Args:
            individual (Individual): an Individual in the set.

        Returns:
            bool: whether the individual exists in the set.
        """
        return individual in self.individuals
    
    def __iter__(self) -> Iterator[Individual]:
        """Provides an iterator for the SetOfIndividuals.

        Returns:
            Interator[Individual]: iterator for the set.
        """
        return IndividualsIterator(self.individuals)#.individuals.keys()
    
    def __len__(self) -> int:
        """Returns the length of the SetOfIndividuals.

        Returns:
            int: _description_
        """
        return len(self.individuals)
    
    def __getitem__(self, item: int | slice) -> Individual:
        """
        Retrieve an agent or a slice of agents from the SetOfIndividuals. Took from mesa.agent.

        Args:
            item (int | slice): The index or slice for selecting agents.

        Returns:
            Agent | list[Agent]: The selected agent or list of agents based on the index or slice provided.
        """
        return list(self.individuals)[item]
    
    def add(self, individual: Individual):
        """Adds an Individual to the SetOfIndividuals.

        Args:
            individual (Individual): individual to add to the set.
        """
        self.individuals.append(individual)
        
    def discard(self, individual: Individual):
        """Eliminates an individual from the set (and from the population). 

        Args:
            individual (Individual): individual to be discarded.
        """
        del self.individuals[individual]
        
    def empty_set(self) -> None:
        self.individuals = []
        # for individual in self.individuals:
        #     self.discard(individual)

    def shuffle(self) -> None:
        random.shuffle(self.individuals)
        
    def sample_and_remove(self, number_of_individuals) -> List[Individual]:
        self.shuffle()
        
        list_of_individuals = []
        for i in range(number_of_individuals):
            individual = self.individuals.pop()
            list_of_individuals.append(individual)
            # self.discard(individual)
            
        return list_of_individuals
        
        