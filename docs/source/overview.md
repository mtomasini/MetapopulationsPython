# Metapypulation: an overview

Metapypulation is a package to simulate the spread of culture in a metapopulation. It supplies a set of tools partly inspired by other frameworks such as [Mesa](https://mesa.readthedocs.io/en/stable/overview.html) which are general-purpose methods to perform agent-based modelling with Python. The main reason to create my own package for this purpose is to change the focus of the tool - population-based simulations instead of individual-based.

## Structure

Metapypulation has three main classes: 

- an `Individual` class, which represents each individual in the metapopulation. 
- a `Subpopulation` class, representing the different discrete subpopulations that compose the metapopulation;
- finally, a `Metapopulation` class, which puts `Individual` and `Subpopulation` together and have individuals interacting in this world. 
