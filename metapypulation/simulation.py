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
    
    Attributes:
        generations (int): Number of generations to simulate.
        number_of_subpopulations (int): Number of subpopulations in the metapopulation.
        interaction_type (str): Type of interaction between individuals.
        carrying_capacities (List[int] | int): Initial population size of each subpopulation.
        replicates (int): Number of replicates to simulate.
        output_path (str): Path of folder in which to save results.
        measure_timing (int): Number of generations between measurements.
        verbose (bool): Whether to print text during the simulation.
        verbose_timing (int): Number of generations between each print statement.
        migration_matrix (str | np.ndarray): Type of migration topology.
        subpop_set_counts (pd.DataFrame): Collects the number of unique set counts per subpopulation averaged over subpopulations.
        subpop_shannon (pd.DataFrame): Collects the Shannon diversity index per subpopulation averaged over subpopulations.
        metapop_set_counts (pd.DataFrame): Collects the number of unique set counts over the whole metapopulation.
        metapop_shannon (pd.DataFrame): Collects the Shannon diversity index over the whole metapopulation.
    """
    def __init__(self, 
                 generations: int,
                 number_of_subpopulations: int, 
                 migration_matrix: str | np.ndarray, 
                 interaction: str, 
                 carrying_capacities: List[int] | int,
                 replicates: int,
                 output_path: str,
                 measure_timing: int = 100,
                 verbose: bool = True,
                 verbose_timing: int = 10000):
        """
        Create a simulation.

        Args:
            generations (int): Number of generations to simulate.
            number_of_subpopulations (int): Number of subpopulations in the metapopulation.
            migration_matrix (str | np.ndarray): Type of migration topology. Either a string to fetch a .csv from the /configs or a numpy array matrix.
            interaction (str): Type of interaction between individuals. Currently accepts only "axelrod_interaction".
            carrying_capacities (List[int] | int): Initial population size of each subpopulation. Either a list with a carrying capacity for each subpopulation, or an int with equal carrying capacity for all subpopulations.
            replicates (int): Number of replicates to simulate.
            output_path (str): Path of folder in which to save results. Creates new folder if it does not exist.
            measure_timing (int, optional): Number of generations between measurements. Defaults to 100.
            verbose (bool, optional): Whether to print text during the simulation. Defaults to True.
            verbose_timing (int, optional): Number of generations between each print statement. Defaults to 10000.  
        """
        self.generations = generations
        self.number_of_subpopulations = number_of_subpopulations
        
        self.interaction_type = interaction
        self.carrying_capacities = carrying_capacities
        self.replicates = replicates
        self.output_path = output_path
        self.measure_timing = measure_timing
        
        self.verbose = verbose
        self.verbose_timing = verbose_timing
        
        match migration_matrix:
            case str():
                self.migration_matrix = np.genfromtxt(f'./configs/{migration_matrix}.csv', delimiter=',')
            case np.ndarray():
                self.migration_matrix = migration_matrix
                
        self.subpop_set_counts = pd.DataFrame()
        self.subpop_shannon = pd.DataFrame()
        self.metapop_set_counts = pd.DataFrame()
        self.metapop_shannon = pd.DataFrame()

        
    def run_replicate(self, replicate_id: int):
        """
        Run one replicate of the simulation.

        Args:
            replicate_id (int): The number of the current replicate (for the output data columns).
        """
        metapopulation = Metapopulation(self.number_of_subpopulations, self.interaction_type, self.migration_matrix, self.carrying_capacities)
        metapopulation.populate()
        
        set_counts = []
        shannon = []
        metapop_counts = []
        metapop_shannon = []
        
        start_time = time.time()
        for t in range(self.generations + 1):
            if self.verbose:
                if t%self.verbose_timing == 0:
                    print(f"Replicate {replicate_id}, gen {t}!")
                    # TODO print other fun stuff
                    
            if t%self.measure_timing == 0:
                set_counts.append(np.mean(metapopulation.traits_sets_per_subpopulation()))
                shannon.append(np.mean(metapopulation.shannon_diversity_per_subpopulation()))
                metapop_counts.append(metapopulation.metapopulation_test_sets())
                metapop_shannon.append(metapopulation.metapopulation_shannon_diversity())
                
            metapopulation.migrate()
            metapopulation.make_interact()
        
        self.subpop_set_counts = pd.concat([self.subpop_set_counts, pd.Series(set_counts, name=replicate_id)], axis=1)
        self.subpop_shannon = pd.concat([self.subpop_shannon, pd.Series(shannon, name=replicate_id)], axis=1)
        self.metapop_set_counts = pd.concat([self.metapop_set_counts, pd.Series(metapop_counts, name=replicate_id)], axis=1)
        self.metapop_shannon = pd.concat([self.metapop_shannon, pd.Series(metapop_shannon, name=replicate_id)], axis=1)
                             
        if self.verbose:
            end_time = time.time()
            total_time = end_time - start_time
            total_time = time.strftime("%H:%M:%S", time.gmtime(total_time))

            print(f"{t} generations ran in {total_time}.")
           

    def run_simulation(self):
        """
        Run all the replicates and print some outputs.
        """
        if self.verbose:
            match self.migration_matrix:
                case str():
                    print(f"Simulating {self.replicates} replicates of the {self.migration_matrix} with {self.number_of_subpopulations}.")
                case np.ndarray():
                    print(f"Simulating {self.replicates} replicates of a custom migration model with {self.number_of_subpopulations}.")
        
        for replicate in range(1, self.replicates + 1):
            self.run_replicate(replicate)
            
        self.save_output()
            
            
    def save_output(self):
        """
        Save output to input folder.
        """
        self.subpop_set_counts.to_csv(f"{self.output_path}_subpop_set_counts.csv", sep=",", index=False)
        self.subpop_shannon.to_csv(f"{self.output_path}_subpop_shannon.csv", sep=",", index=False)
        self.metapop_set_counts.to_csv(f"{self.output_path}_metapop_set_counts.csv", sep=",", index=False)
        self.metapop_shannon.to_csv(f"{self.output_path}_metapop_shannon.csv", sep=",", index=False)