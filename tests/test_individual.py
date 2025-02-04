import numpy as np
import random
from metapypulation.individual import Individual

def test_axelrod_interaction():
    
    individual_1 = Individual(1, 1, 5, 10)
    individual_2 = Individual(1, 1, 5, 10)
    
    # modify features to something I can control
    individual_1.features = np.array([0, 0, 0, 0, 1])
    individual_2.features = np.array([0, 0, 0, 0, 0])
    
    random.seed(100)
    for i in range(10):
        individual_1.axelrod_interaction(individual_2)
    
    assert np.allclose(individual_1.features, individual_2.features)
    assert individual_1.number_of_changes == 1
    assert individual_2.number_of_changes == 0


def test_init():
    individual_1 = Individual(1, 1, 5, 10)
    individual_2 = Individual(1, 1, 5, 10, features=[1, 5, 3, 0, 9])

    assert len(individual_1.features) == individual_1.number_of_features
    assert individual_2.features == [1, 5, 3, 0, 9]