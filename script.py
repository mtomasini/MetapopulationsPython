import matplotlib.pyplot as plt
import numpy as np
import time

from metapypulation.simulation import Simulation

total_population = 800
replicates = 1
migrations = ['island', 'stepping_stone']
interactions = ['neutral_interaction', 'axelrod_interaction']

start_time = time.time()

for migration in migrations:
    for interaction in interactions:
        
        subpopulations = 8
        rate_of_migration = 0.001

        carrying_capacity = int(np.ceil(total_population / subpopulations)) # [283, 39, 39, 39]# 
        generations = 200000
        burn_in = 50000

        simulation = Simulation(generations, 
                                subpopulations, 
                                migration, 
                                interaction,
                                carrying_capacity,
                                replicates,
                                f"./Outputs/TAG2024/01-neutral-axelrod/{subpopulations}subpop_{migration}_{interaction}",
                                burn_in = burn_in,
                                migration_rate = rate_of_migration)

        simulation.run_simulation()

    #f"./Outputs/SourceSink/pop{total_population}/{migrations}/{subpopulations}subpop_m1e-3_burnin_{carrying_capacity[0]}",
                            
end_time = time.time() - start_time
hours = round(end_time//3600)
minutes = round(end_time//60)
seconds = round(end_time) - hours*3600 - minutes*60
print(f"Simulation of {replicates} replicates finished in {hours}h, {minutes}m and {seconds}s")