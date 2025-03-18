import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from metapypulation.simulation import Metapopulation

verbose = True
verbose_timing = 10000
measure_timing = 100

total_population = 800
replicates = 10
save_output = True
interactions = ['neutral_interaction'] # 'axelrod_interaction'
number_of_subpopulations = 8
migration_rates = [0.0001]
mutation_rates = 0.0005

burn_in = 50000
pulse_length = 100
number_of_pulses = 5
settling_period = 10000 - pulse_length # 10000

start_time = time.time()

count = 0

title = "singleConnection"
migration_config = np.genfromtxt(f"./configs/maritime_configs/{title}.csv", delimiter=",")

for interaction in interactions:
    for rate_of_migration in migration_rates:
        
        subpop_set_counts_df = pd.DataFrame()
        subpop_gini_df = pd.DataFrame()
        metapop_set_counts_df = pd.DataFrame()
        metapop_gini_df = pd.DataFrame()

        carrying_capacity = int(np.ceil(total_population / number_of_subpopulations)) # [283, 39, 39, 39]# 
        
        # generations = 300000# burn_in + number_of_pulses*(pulse_length + settling_period)
        
        migration_matrix = migration_config*rate_of_migration

        for replicate_id in range(replicates):
            # create metapopulation
            metapopulation = Metapopulation(number_of_subpopulations, interaction, migration_matrix, 
                                            carrying_capacity, mutation_rate = mutation_rates)
            metapopulation.populate()
            
            set_counts = []
            gini = []
            metapop_counts = []
            metapop_gini = []

            t = 0
            for gen in range(burn_in):
                metapopulation.make_interact()

                if verbose:
                    if t%verbose_timing == 0:
                        print(f"Replicate {replicate_id}, gen {t}!")
                        print(f"Pop size of metapopulation {metapopulation.get_metapopulation_size()}")
                        # TODO print other fun stuff

                if t%measure_timing == 0:
                    set_counts.append(np.mean(metapopulation.traits_sets_per_subpopulation()))
                    gini.append(np.mean(metapopulation.gini_diversity_per_subpopulation()))
                    metapop_counts.append(metapopulation.metapopulation_test_sets())
                    metapop_gini.append(metapopulation.metapopulation_gini_diversity())
                        
                t += 1
            
            # print(metapopulation.count_origin_id_spread())

            for i in range(1, number_of_pulses + 1):
                for gen in range(pulse_length + settling_period):
                    if t < burn_in + i*(pulse_length) + (i-1)*settling_period:
                        metapopulation.migration_matrix = np.genfromtxt(f"./configs/maritime_configs/{title}.csv", delimiter=",") * rate_of_migration
                        metapopulation.migrate()
                        metapopulation.make_interact()
                    elif t >= burn_in + i*(pulse_length) + (i-1)*settling_period:
                        metapopulation.migration_matrix = np.genfromtxt(f"./configs/maritime_configs/seaConnection.csv", delimiter=",") * rate_of_migration
                        metapopulation.migrate()
                        metapopulation.make_interact()

                    if verbose:
                        if t%verbose_timing == 0:
                            print(f"Replicate {replicate_id}, gen {t}!")
                            print(f"Pop size of metapopulation {metapopulation.get_metapopulation_size()}")
                            #print(metapopulation.count_origin_id_spread())
                            # TODO print other fun stuff

                    if t%measure_timing == 0:
                        set_counts.append(np.mean(metapopulation.traits_sets_per_subpopulation()))
                        gini.append(np.mean(metapopulation.gini_diversity_per_subpopulation()))
                        metapop_counts.append(metapopulation.metapopulation_test_sets())
                        metapop_gini.append(metapopulation.metapopulation_gini_diversity())

                    t += 1
            
            subpop_set_counts_df = pd.concat([subpop_set_counts_df, pd.Series(set_counts, name=replicate_id)], axis=1)
            subpop_gini_df = pd.concat([subpop_gini_df, pd.Series(gini, name=replicate_id)], axis=1)
            metapop_set_counts_df = pd.concat([metapop_set_counts_df, pd.Series(metapop_counts, name=replicate_id)], axis=1)
            metapop_gini_df = pd.concat([metapop_gini_df, pd.Series(metapop_gini, name=replicate_id)], axis=1)
                                
            if verbose:
                print(f"Generation reached: {t}")
                end_time = time.time()
                total_time = end_time - start_time
                total_time = time.strftime("%H:%M:%S", time.gmtime(total_time))

                print(f"{t} generations ran in {total_time}.")

            # print(metapopulation.count_origin_id_spread())

        if save_output:
            subpop_set_counts_df.to_csv(f"./Outputs/Kiel2025/{title}/{interaction}_{rate_of_migration}_{number_of_pulses}pulses_{pulse_length}gen_subpop_set_counts.csv", sep=",")
            subpop_gini_df.to_csv(f"./Outputs/Kiel2025/{title}/{interaction}_{rate_of_migration}_{number_of_pulses}pulses_{pulse_length}gen_subpop_gini.csv", sep=",")
            metapop_set_counts_df.to_csv(f"./Outputs/Kiel2025/{title}/{interaction}_{rate_of_migration}_{number_of_pulses}pulses_{pulse_length}gen_metapop_set_counts.csv", sep=",")
            metapop_gini_df.to_csv(f"./Outputs/Kiel2025/{title}/{interaction}_{rate_of_migration}_{number_of_pulses}pulses_{pulse_length}gen_metapop_gini.csv", sep=",")

        # subpop_gini_df.to_csv("test.csv")
                                    
end_time = time.time() - start_time
hours = round(end_time//3600)
minutes = round(end_time//60) - hours*60
seconds = round(end_time) - hours*3600 - minutes*60
print(f"Simulation of {count} sets of parameters, {replicates} replicates each, finished in {hours}h, {minutes}m and {seconds}s")