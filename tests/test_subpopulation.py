from metapypulation.individual import Individual
from metapypulation.subpopulation import Subpopulation

def test_receive_migrants():
    giving_subpopulation = Subpopulation(1, "axelrod_interaction")
    receiving_subpopulation = Subpopulation(2, "axelrod_interaction")
    migration_rate = 0
    
    for i in range(100):
        test_individual = Individual(i, 1, 1, 1)
        giving_subpopulation.add_individual(test_individual)
    for i in range(100):
        test_individual = Individual(i, 2, 1, 1)
        receiving_subpopulation.add_individual(test_individual)
    
    receiving_subpopulation.receive_migrants(giving_subpopulation, migration_rate)
    assert receiving_subpopulation.get_current_number_of_migrants() == 0
    
    migration_rate = 0.1
    receiving_subpopulation.receive_migrants(giving_subpopulation, migration_rate)
    # the population size in the giving subpopulation after this step is the initial population (100) minus the number of migrants in the receiving_population
    assert giving_subpopulation.get_population_size() == 100 - receiving_subpopulation.get_current_number_of_migrants()
    
    # all individuals in the giving_subpopulation have original deme = 1
    for individual in giving_subpopulation.population:
        assert individual.original_deme_id == 1
    
    # all individuals in the incoming migrants have original deme = 1
    for individual in receiving_subpopulation.incoming_migrants:
        assert individual.original_deme_id == 1
        
        
def test_incorporate_migrants_in_population():
    receiving_subpopulation = Subpopulation(1, "axelrod_interaction")
    number_of_migrants = 10
    
    for i in range(number_of_migrants):
        test_individual = Individual(i, 1, 1, 1)
        receiving_subpopulation.incoming_migrants.add(test_individual)
    
    assert receiving_subpopulation.get_current_number_of_migrants() == number_of_migrants    
    
    receiving_subpopulation.incorporate_migrants_in_population()
    
    assert receiving_subpopulation.get_population_size() == number_of_migrants
    assert receiving_subpopulation.get_current_number_of_migrants() == 0