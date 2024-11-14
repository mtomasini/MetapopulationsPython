import matplotlib.pyplot as plt
import numpy as np

from metapypulation.simulation import Simulation

total_population = 1200

#migrations_island = np.genfromtxt('./configs/island_model.csv', delimiter=',')
#migrations_stepping = np.genfromtxt('./configs/stepping_stone.csv', delimiter=',')

for migrations in ['island']:
        
    subpopulations = 4
    rate_of_migration = 0.005

    carrying_capacity = int(np.ceil(total_population / subpopulations)) # [283, 39, 39, 39]# 
    generations = 200000
    burn_in = 50000

    simulation = Simulation(generations, 
                            subpopulations, 
                            migrations, 
                            "neutral_interaction",
                            carrying_capacity,
                            10,
                            f"./Outputs/SourceSink/pop{total_population}/{migrations}/{subpopulations}subpop_m1e-3_burnin_{carrying_capacity[0]}",
                            burn_in = burn_in,
                            migration_rate = rate_of_migration)

    simulation.run_simulation()