"""
A module containing the tools to simulate a metapopulation and output the result in data tables.
"""

import numpy as np
import pandas as pd
from typing import List
import time

from .metapopulation import Metapopulation
from .subpopulation import Subpopulation
from .individual import Individual

class Simulation():
    """
    Base class for the simulation of the metapopulation.
    
    
    """
    def __init__(self, 
                 generations: int,
                 number_of_subpopulations: int, 
                 migration_matrix: str | np.ndarray, 
                 interaction: str, 
                 carrying_capacities: List[int] | int,
                 replicates: int,
                 output_path: str,
                 verbatim: bool = True,
                 verbatim_timing: int = 1000):
        self.generations = generations
        self.number_of_subpopulations = number_of_subpopulations
        
        self.interaction_type = interaction
        self.carrying_capacities = carrying_capacities
        self.replicates = replicates
        self.output_path = output_path
        
        self.verbatim = verbatim
        self.verbatim_timing = verbatim_timing
        
        match migration_matrix:
            case str():
                self.migration_matrix = np.genfromtxt(f'./configs/{migration_matrix}.csv', delimiter=',')
            case np.ndarray:
                self.migration_matrix = migration_matrix
    
        
    def run_replicate():
        pass