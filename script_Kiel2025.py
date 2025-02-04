import matplotlib.pyplot as plt
import numpy as np
import time

from metapypulation.simulation import Simulation

total_population = 200
replicates = 1
#migrations = ['island'] # 'stepping_stone'
interactions = ['neutral_interaction'] # 'axelrod_interaction'
#number_of_subpopulations = [4]
subpopulations = 4
population_sizes = [[50, 50, 50, 50]]

start_time = time.time()

count = 0

for interaction in interactions:
    for rate_of_migration in [0.001, 0.1]:
        # rate_of_migration = 0.001

        carrying_capacity = int(np.ceil(total_population / subpopulations)) # [283, 39, 39, 39]# 
        generations = 200000 #350000
        burn_in = 0

        # create one big simulation
        simulation = Simulation(generations = generations, 
                                number_of_subpopulations=subpopulations, 
                                migration_matrix = migration, 
                                interaction = interaction,
                                carrying_capacities = carrying_capacity,
                                replicates = replicates,
                                output_path = f"./Outputs/{subpopulations}subpop_popsize{population_sizes[0]}_{migration}_{interaction}_{rate_of_migration}_noburnin",  #TAG2024/04-migration-rates/{subpopulations}subpop_{migration}_{interaction}_m{rate_of_migration}",
                                burn_in = burn_in,
                                migration_rate = rate_of_migration)

        # modify individuals in simulation
        

        simulation.run_simulation()
        count = count + 1
    #f"./Outputs/SourceSink/pop{total_population}/{migrations}/{subpopulations}subpop_m1e-3_burnin_{carrying_capacity[0]}",
                            
end_time = time.time() - start_time
hours = round(end_time//3600)
minutes = round(end_time//60) - hours*60
seconds = round(end_time) - hours*3600 - minutes*60
print(f"Simulation of {count} sets of parameters, {replicates} replicates each, finished in {hours}h, {minutes}m and {seconds}s")