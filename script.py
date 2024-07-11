import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from metapypulation.subpopulation import Subpopulation
from metapypulation.individual import Individual
from metapypulation.metapopulation import Metapopulation

migrations = np.genfromtxt('./configs/island_model.csv', delimiter=',')

migrations = migrations

metapop = Metapopulation(4, "axelrod_interaction", migrations, carrying_capacities=100)
metapop.populate()

shannon = []
set_counts = []

start_time = time.time()
for t in range(300001):
    if t%100 == 0:
        set_counts.append(metapop.metapopulation_count_traits_sets())
        shannon.append(metapop.metapopulation_shannon_diversity())
    if t%50000 == 0:
        print(f"Gen {t}!")
        for subpopulation in metapop.subpopulations:
            print(f"The current size of pop {subpopulation.id} is {subpopulation.get_population_size()}")
            sub_id = []
            for ind in subpopulation.population.individuals:
                sub_id.append(ind.original_deme_id)
            indexes, counts = np.unique(sub_id, return_counts=True)
            print(f"The current deme index present in population {subpopulation.id} are {indexes} with {counts} counts.")
    
    metapop.migrate()
    metapop.make_interact()
    
    
end_time = time.time()
total_time = end_time - start_time
total_time = time.strftime("%H:%M:%S", time.gmtime(total_time))

print(f"{t} generations ran in {total_time}.")

counts_df = pd.DataFrame(set_counts)
counts_df.to_csv('./Outputs/island.csv', index=False)
# print(counts_df)
# counts_df.plot()
# plt.show()