import numpy as np
from metapypulation.simulation import Simulation

def test_create_migration_table():
    simulation = Simulation(100, 3, 'island', 'axelrod_interaction', 100, 1, 'something.csv')
    assert simulation.migration_matrix.shape == (3,3)
    assert np.allclose(simulation.migration_matrix[0], np.array([0.0, 0.001, 0.001]))
    
    simulation = Simulation(100, 7, 'stepping_stone', 'axelrod_interaction', 100, 1, 'something.csv')
    assert simulation.migration_matrix.shape == (7,7)
    assert np.allclose(simulation.migration_matrix[0], np.array([0.0, 0.001, 0.0, 0.0, 0.0, 0.0, 0.0]))
    