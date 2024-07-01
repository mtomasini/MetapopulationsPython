"""
A module containing the subpopulation class.
"""

from collections.abc import MutableSet
import numpy as np
from typing import Tuple

from .individual import Individual


class Subpopulation():
    def __init__(self, id: int, coordinates: Tuple[int, int], migration_mapping: np.ndarray = None):
        self.id = id
        self.coordinates = coordinates
        self.migration_mapping = migration_mapping
        self.population = IndividualsInPopulation(self)
        

class IndividualsInPopulation(MutableSet):
    def __init__(self, deme: Subpopulation):
        self.individuals = []
        self.deme = deme.id
        
    def __contains__(self, individual: Individual):
        return individual in self.individuals
    
    def __iter__(self):
        return self.individuals.keys()
    
    def __len__(self):
        return len(self.individuals)
    
    def add(self, individual: Individual):
        self.individuals.append(individual)
        
    def discard(self, individual: Individual):
        del self.individuals[individual]