# Metapypulation: an overview

Metapypulation is a package to simulate the spread of culture in a metapopulation. It supplies a set of tools partly inspired by other frameworks such as [Mesa](https://mesa.readthedocs.io/en/stable/overview.html) which are general-purpose methods to perform agent-based modelling with Python. The main reason to create my own package for this purpose is to change the focus of the tool - population-based simulations instead of individual-based.

## Structure

Metapypulation has three main classes:

- an [`Individual`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.individual) class, which represents each individual in the metapopulation.
- a [`Subpopulation`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.subpopulation) class, representing the different discrete subpopulations that compose the metapopulation;
- finally, a [`Metapopulation`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.metapopulation) class, which puts `Individual` and `Subpopulation` together and have individuals interacting in this world.

In addition, I provide a [`Simulation`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.simulation) class, which allows to run a simulation with several replicates, which outputs different measurements ([see below](#diversity-measures)). The class also provides some quick tools to plot the results of the simulation.

## Cultural traits

Currently, each individual's culture is represented by a set of {math}`N` features. Each feature in turn can assume one of {math}`\nu` traits. These features represent different (assumed) independent facets of culture: one could be language, burial tradition, boat building features, *etc*. So each individual is currently represented by a vector of integers.

### Axelrod model

While we plan on adding several different ways for individuals to interact and change their traits, as of July 2024 the only such way to interact is shaped upon the **Axelrod model of culture dissemination**. In this model, at each generation an individual is chosen at random to copy a trait from a neighboring source on a lattice; the copy occurs with a probability proportional to the total similarity of the two random individuals. This mimicks homophily - the principle by which two individuals that resemble each other have a higher chance of having an exchange than two individuals that are completely different. In the metapopulation model that I developed, for each subpopulation we pick two random individuals that will act as target and source of the copy.

### Diversity measures

Currently, there are two diversity measures implemented at the level of both the subpopulation and the whole metapopulation. The first is the Shannon diversity index, which for each feature is measured as

```{math}
H^{\prime} = - \sum_{i = 1}^{\nu} p_i \ln p_i ,
```

where {math}`p_i` is the frequency of trait {math}`i` in the subpopulation / metapopulation. Then, the Shannon diversity index that we measure is the average of the index for each trait,

```{math}
\bar{H} = H^{\prime} .
```

The second diversity measure that we calculate is the number of unique sets of traits. This is done through the function `np.unique(..., return_counts = True)`.
