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

### Neutral model

The Neutral model follows loosely the set up selected by other authors working on the spread of cultural traits (_e.g._ *Patterns in space and time: simulating cultural transmission in archaeology*, Marko Porčić). We use the simplest model where one focal individual at random in each subpopulation and each time-step copies one trait at random from another individual in the same subpopulation. The model allows for copying errors with rate {math}`\mu`: if a copying error occurs, instead of copying a trait from another individual, the focal individual changes the trait at the feature in focus with a random trait between the available ones. 

### Axelrod model

While we plan on adding several different ways for individuals to interact and change their traits, as of July 2024 the only such way to interact is shaped upon the **Axelrod model of culture dissemination** (*The Dissemination of Culture: A Model with Local Convergence and Global Polarization*, Robert Axelrod (1997), The Journal of Conflict Resolution, vol. 41, no. 2). In this model, at each generation an individual is chosen at random to copy a trait from a neighboring source on a lattice; the copy occurs with a probability proportional to the total similarity of the two random individuals. This mimicks homophily - the principle by which two individuals that resemble each other have a higher chance of having an exchange than two individuals that are completely different. In the metapopulation model that I developed, for each subpopulation we pick two random individuals that will act as target and source of the copy. Here too, copying errors occur with rate {math}`\mu`.

### Diversity measures

Currently, there are two diversity measures implemented at the level of both the subpopulation and the whole metapopulation. The first is the Shannon diversity index, which for each feature is measured as

```{math}
H^{\prime} = - \sum_{i = 1}^{\nu} p_i \ln p_i ,
```

where {math}`p_i` is the frequency of trait {math}`i` in the subpopulation / metapopulation. Then, the Shannon diversity index that we measure is the average of the index for each trait,

```{math}
\bar{H} = H^{\prime} .
```

The second diversity measure that we calculate is the number of unique sets of traits, {math}`K`. In code, this is done through the function `np.unique(..., return_counts = True)`. 
We also implemented the (inversed) Simpson's diversity index, defined as 

```{math}
S = \frac{N(N-1)}{\sum_{k}n_k(n_k-1)} ,
```

where {math}`n_k` is the number of individuals with the set of traits {math}`k`. This is implemented both at the level of the subpopulation and of the metapopulation.