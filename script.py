import matplotlib.pyplot as plt
import numpy as np

from metapypulation.simulation import Simulation

total_population = 400

#migrations_island = np.genfromtxt('./configs/island_model.csv', delimiter=',')
#migrations_stepping = np.genfromtxt('./configs/stepping_stone.csv', delimiter=',')

for migrations in ['stepping_stone']:  
        
    subpopulations = 4
    rate_of_migration = 0.001

    carrying_capacity = int(np.ceil(total_population / subpopulations))
    generations = 200000
    burn_in = 50000

    simulation = Simulation(generations, 
                            subpopulations, 
                            migrations, 
                            "axelrod_interaction",
                            carrying_capacity,
                            10,
                            f"./Outputs/pop{total_population}/{migrations}/{subpopulations}subpop_m1e-3_burnin",
                            burn_in = burn_in,
                            migration_rate = rate_of_migration)

    simulation.run_simulation()
