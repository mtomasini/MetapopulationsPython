import numpy as np

from metapypulation.metapopulation import Metapopulation

def test_populate():
    carrying_capacity = 200
    migrations = np.genfromtxt('./tests/test_configs/island_model.csv', delimiter=',')
    metapop = Metapopulation(4, "axelrod_interaction", migrations, carrying_capacities=carrying_capacity)
    for subpopulation in metapop.subpopulations:
        assert subpopulation.get_population_size() == 0
    
    metapop.populate()
    for subpopulation in metapop.subpopulations:
        assert subpopulation.get_population_size() == carrying_capacity


def test_populate_with_custom_traits():
    carrying_capacity = 200
    migrations = np.genfromtxt('./tests/test_configs/island_model.csv', delimiter=',')
    # initialize metapop with 8 traits from 50 to 57
    metapop = Metapopulation(4, "axelrod_interaction", migrations, carrying_capacities=carrying_capacity, min_trait=50, max_trait=57)
    for subpopulation in metapop.subpopulations:
        assert subpopulation.get_population_size() == 0
    
    metapop.populate()
    for subpopulation in metapop.subpopulations:
        assert subpopulation.get_population_size() == carrying_capacity
        
        for individual in subpopulation.population:
            assert any(y <= 57 for y in individual.features)
            assert any(y >= 50 for y in individual.features)
            assert len(individual.features) == 5
            assert individual.number_of_traits == 8
    
    
def test_migrate():
    migrations = np.genfromtxt('./tests/test_configs/island_model.csv', delimiter=',')
    metapop = Metapopulation(4, "axelrod_interaction", migrations, carrying_capacities=100)
    
    metapop.populate()
    metapop.migrate()
    
    total_size = 0
    for subpopulation in metapop.subpopulations:
        total_size += subpopulation.get_population_size()
        
    assert total_size == 100*4
