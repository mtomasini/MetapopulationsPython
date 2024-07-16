import matplotlib.pyplot as plt
import numpy as np

from metapypulation.simulation import Simulation

total_population = 1000

migrations = np.genfromtxt('./configs/island_model.csv', delimiter=',')
subpopulations = migrations.shape[0]
carrying_capacity = np.ceil(total_population / subpopulations)

generations = 100000

simulation = Simulation(generations, 
                        migrations.shape[0], 
                        migrations, 
                        "axelrod_interaction",
                        carrying_capacity,
                        10,
                        f"./Outputs/pop{total_population}")