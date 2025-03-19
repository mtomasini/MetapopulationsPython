"""
Script: simulate a metapopulation with a migration-less burn-in phase, a variable length of evolution (neutral or Axelrod) followed 
by the introduction of a new set of features. I am testing two things: 

1) What is the probability of emergence of the new feature under each model?
2) What is the speed of emergence of the new feature under each model?

To insert a new mutation:
- select a deme (default: deme 3)
- select an individual at random
- change one of its traits at random to a new value

"""

import math
import matplotlib.pyplot as plt
import numpy as np

from metapypulation.metapopulation import Metapopulation
from metapypulation.subpopulation import Subpopulation
from metapypulation.individual import Individual

total_population = 400
interaction = "neutral_interaction"
N_subpopulations = 8
subpop_size = math.ceil(total_population / N_subpopulations)
deme_of_new_mutation = 3 # 4th deme of 8
new_value = 35

migrations = np.genfromtxt('./configs/stepping_stone_8pop.csv', delimiter=',')
migrations_zero = np.zeros((8,8))

burn_in = 10000
first_epoch = 0
burn_out = 100000 #2000000

replicates = 1000

successes = []

for i in range(1, replicates + 1):
    metapop = Metapopulation(N_subpopulations, interaction, migration_matrix = migrations, carrying_capacities=subpop_size)
    metapop.populate()

    counts_pop_1 = []
    counts_pop_2 = []
    counts_pop_3 = []
    counts_pop_4 = []
    counts_pop_5 = []
    counts_pop_6 = []
    counts_pop_7 = []
    counts_pop_8 = []
    counts_metapop = []

    subpops_with_mutation = []

    # BURN-IN PHASE
    for t in range(burn_in):
        if t%1000 == 0:
            counts_pop_1.append(metapop.subpopulations[0].count_traits_sets())
            counts_pop_2.append(metapop.subpopulations[1].count_traits_sets())
            counts_pop_3.append(metapop.subpopulations[2].count_traits_sets())
            counts_pop_4.append(metapop.subpopulations[3].count_traits_sets())
            counts_pop_5.append(metapop.subpopulations[4].count_traits_sets())
            counts_pop_6.append(metapop.subpopulations[5].count_traits_sets())
            counts_pop_7.append(metapop.subpopulations[6].count_traits_sets())
            counts_pop_8.append(metapop.subpopulations[7].count_traits_sets())
            counts_metapop.append(metapop.metapopulation_count_sets())
            subpops_with_mutation.append(0)
        # if t%50000 == 0:
        #     print(f"Gen {t}!")
        #     for subpopulation in metapop.subpopulations:
        #         print(f"The current number of sets in pop {subpopulation.id} is {subpopulation.count_traits_sets()}")
                
        # metapop.migrate()
        metapop.make_interact()
        
    # FIRST INTERACTION PHASE
    for t in range(burn_in, burn_in + first_epoch):
        if t%1000 == 0:
            counts_pop_1.append(metapop.subpopulations[0].count_traits_sets())
            counts_pop_2.append(metapop.subpopulations[1].count_traits_sets())
            counts_pop_3.append(metapop.subpopulations[2].count_traits_sets())
            counts_pop_4.append(metapop.subpopulations[3].count_traits_sets())
            counts_pop_5.append(metapop.subpopulations[4].count_traits_sets())
            counts_pop_6.append(metapop.subpopulations[5].count_traits_sets())
            counts_pop_7.append(metapop.subpopulations[6].count_traits_sets())
            counts_pop_8.append(metapop.subpopulations[7].count_traits_sets())
            counts_metapop.append(metapop.metapopulation_count_sets())
            subpops_with_mutation.append(0)
        # if t%50000 == 0:
        #     print(f"Gen {t}!")
        #     for subpopulation in metapop.subpopulations:
        #         print(f"The current number of sets in pop {subpopulation.id} is {subpopulation.count_traits_sets()}")
                
        metapop.migrate()
        metapop.make_interact()

    
    # INTRODUCE NEW INDIVIDUAL     
    # select tandom individual in a deme
    deme_selected = metapop.subpopulations[deme_of_new_mutation]
    random_individual_id = np.random.choice(range(deme_selected.get_population_size()))
    
    # change individual first feature
    deme_selected.population[random_individual_id].features[0] = new_value
    #subpops_with_mutation[-1] = 1

    mutation_has_died = False
    # 
    for t in range(burn_in + first_epoch, burn_in + first_epoch + burn_out):

        if t%1000 == 0:
            counts_pop_1.append(metapop.subpopulations[0].count_traits_sets())
            counts_pop_2.append(metapop.subpopulations[1].count_traits_sets())
            counts_pop_3.append(metapop.subpopulations[2].count_traits_sets())
            counts_pop_4.append(metapop.subpopulations[3].count_traits_sets())
            counts_pop_5.append(metapop.subpopulations[4].count_traits_sets())
            counts_pop_6.append(metapop.subpopulations[5].count_traits_sets())
            counts_pop_7.append(metapop.subpopulations[6].count_traits_sets())
            counts_pop_8.append(metapop.subpopulations[7].count_traits_sets())
            counts_metapop.append(metapop.metapopulation_count_sets())
        
            feature_tests = []
            for subpop in metapop.subpopulations:
                feature_tests.append(subpop.is_trait_in_subpopulation(new_value))

            if not any(feature_tests):
                subpops_with_mutation.append(0)
                mutation_has_died = True
            else:
                subpops_with_mutation.append(sum(feature_tests))


        # if t%50000 == 0:
        #     print(f"Gen {t + burn_in}!")
        #     for subpopulation in metapop.subpopulations:
        #         print(f"The current number of sets in pop {subpopulation.id} is {subpopulation.count_traits_sets()}")
                # sub_id = []
                # for ind in subpopulation.population.individuals:
                #     sub_id.append(ind.original_deme_id)
                # indexes, counts = np.unique(sub_id, return_counts=True)
                # print(f"The current deme index present in population {subpopulation.id} are {indexes} with {counts} counts.")
        
        metapop.migrate()
        metapop.make_interact()

        if mutation_has_died:
            print(f"Finished in generation {t + burn_in + first_epoch}")
            break
        
    if t == burn_in + first_epoch + burn_out - 1:
        print(f"Replicate {i}: mutation present in {subpops_with_mutation[-1]} demes")
        successes.append(1)
        # plt.plot(subpops_with_mutation)
        # plt.xlabel("generations (x1000)")
        # plt.ylabel("number of subpopulations where the new trait can be found")
        # plt.show()

success = sum(successes)
print(success / replicates)

# plt.plot(subpops_with_mutation)
# plt.xlabel("generations (x1000)")
# plt.ylabel("number of subpopulations where the new trait can be found")
# plt.show()