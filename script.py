import matplotlib.pyplot as plt
import numpy as np

from metapypulation.simulation import Simulation

total_population = 400

#migrations_island = np.genfromtxt('./configs/island_model.csv', delimiter=',')
#migrations_stepping = np.genfromtxt('./configs/stepping_stone.csv', delimiter=',')

for migrations in ['island_model', 'stepping_stone']:  
        
    subpopulations = 8

    carrying_capacity = int(np.ceil(total_population / subpopulations))
    generations = 200000

    simulation = Simulation(generations, 
                            subpopulations, 
                            migrations, 
                            "axelrod_interaction",
                            carrying_capacity,
                            10,
                            f"./Outputs/pop{total_population}/{migrations}/4subpop")

    simulation.run_simulation()
