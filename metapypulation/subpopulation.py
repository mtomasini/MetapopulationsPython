"""
A module containing the subpopulation class.
"""

from collections.abc import Iterator, MutableSet
import numpy as np
import random
from typing import List, Tuple

from .individual import Individual


class Subpopulation():
    def __init__(self, id: int):
        self.id = id
        self.population = SetOfIndividuals(self)
        self.outgoing_migrants = SetOfIndividuals(self)
        
        
    def get_population_size(self):
        return len(self.population)
    
    
    def get_current_number_of_migrants(self):
        return len(self.outgoing_migrants)
    
        
    def list_migrants(self, migration_rate: float) -> None:
        """This function creates a list of migrants that will be sent out of the subpopulation.

        Args:
            migration_rate (float): the migration rate is defined as the expected percentage of population that will migrate at each generation.

        Returns:
            List[Individual]: a simple list of individuals from the subpopulation.
        """
        # self.population.shuffle()
        size = self.get_population_size()
        number_of_migrants = np.random.binomial(size, migration_rate)
        # indeces_to_migrate = random.sample(range(size), number_of_migrants)
        if number_of_migrants > 0:
            individuals_to_remove = self.population.sample_and_remove(number_of_migrants)
            for individual in individuals_to_remove:
                self.outgoing_migrants.add(individual)
            
                
    def incorporate_migrants_in_population(self, incoming_migrants: "SetOfIndividuals") -> None:
        for individual in incoming_migrants:
            self.population.add(individual)
        
        incoming_migrants.empty_set()
        
      
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
    
    # def __next__(self):
    #     if len(self.individuals) == 0:
    #         raise StopIteration
        
    #     return self.individuals[0]
    
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
        
        