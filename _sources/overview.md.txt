# Metapypulation: an overview

Metapypulation is a package to simulate the spread of culture in a metapopulation. It supplies a set of tools partly inspired by other frameworks such as [Mesa](https://mesa.readthedocs.io/en/stable/overview.html) which are general-purpose methods to perform agent-based modelling with Python. The main reason to create my own package for this purpose is to change the focus of the tool - population-based simulations instead of individual-based.

## Structure

Metapypulation has three main classes:

- an [`Individual`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.individual) class, which represents each individual in the metapopulation.
- a [`Subpopulation`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.subpopulation) class, representing the different discrete subpopulations that compose the metapopulation;
- finally, a [`Metapopulation`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.metapopulation) class, which puts `Individual` and `Subpopulation` together and have individuals interacting in this world.

In addition, I provide a [`Simulation`](https://mtomasini.github.io/MetapopulationsPython/metapypulation.html#module-metapypulation.simulation) class, which allows to run a simulation with several replicates, which outputs different measurements ([see below](#diversity-measures)). The class also provides some quick tools to plot the results of the simulation.

## The spread of cultural traits

Currently, each individual's culture is represented by a set of {math}`N` features. Each feature in turn can assume one of {math}`\nu` traits. These features represent different (assumed) independent facets of culture: one could be language, burial tradition, boat building features, *etc*. So each individual is currently represented by a vector of integers.

### Neutral model

The Neutral model follows loosely the set up selected by other authors working on the spread of cultural traits (_e.g._ *Patterns in space and time: simulating cultural transmission in archaeology*, Marko Porčić). We use the simplest model where one focal individual at random in each subpopulation and each time-step copies one trait at random from another individual in the same subpopulation. The model allows for copying errors with rate {math}`\mu`: if a copying error occurs, instead of copying a trait from another individual, the focal individual changes the trait at the feature in focus with a random trait between the available ones. 

### Axelrod model

While we plan on adding several different ways for individuals to interact and change their traits, as of July 2024 the only such way to interact is shaped upon the **Axelrod model of culture dissemination** (*The Dissemination of Culture: A Model with Local Convergence and Global Polarization*, Robert Axelrod (1997), The Journal of Conflict Resolution, vol. 41, no. 2). In this model, at each generation an individual is chosen at random to copy a trait from a neighboring source on a lattice; the copy occurs with a probability proportional to the total similarity of the two random individuals. This mimicks homophily - the principle by which two individuals that resemble each other have a higher chance of having an exchange than two individuals that are completely different. In the metapopulation model that I developed, for each subpopulation we pick two random individuals that will act as target and source of the copy. Here too, copying errors occur with rate {math}`\mu`.

### Diversity measures

Currently, we have implemented a few diversity measures at the level of both the subpopulation and the whole metapopulation (to avoid repeating "subpopulation / metapopulation", we refer to either as the "reference population" for the measure. 

#### Count of sets
The first measure that we implemented is the number of unique sets of traits, {math}`K`. In code, this is done through the function `np.unique(..., return_counts = True)`. 

#### Shannon diversity
The second diversity index that we have implemented is the Shannon diversity index, which measures the entropy in the reference population. For {math}`K` sets of traits,

```{math}
H^{\prime} = - \sum_{i = 1}^{K} p_i \ln p_i ,
```

where {math}`p_i` is the frequency of a type of individual {math}`i` in the subpopulation / metapopulation. Shannon is a measure of how "easy" it is, given an individual of type `j`, to predict the set of traits of another individual in the same reference population.

#### Simpson index
We also implemented the Simpson's diversity index, defined as 

```{math}
S = \sum_{i = 1}^{K} p^2_i .
```

The Simpson index is bound between 0 and 1, and represents the probability that two individuals in the same reference population have the same set of traits.

#### Gini-Simpson index
The Gini-Simpson index is simply the complement of the Simpson index, that is it measures the probability that two random indeividuals in the same reference population do not share a set of traits. This is calculated as

```{math}
G = 1 - \sum_{i = 1}^{K} p^2_i = 1 - S.
```

#### {math}`\beta`-diversity
{math}`\beta`-diversity is a ratio between diersity over the whole metapopulation and the diversity per subpopulation. We implemented the diversity index suggested by Whittaker (1960; see also Wilson and Shmida, 1984):

```{math}
\beta_W = \frac{K_m}{\bar{K}_s} - 1
```
where {math}`K_m` is the number of sets of traits in the whole metapopulation, and {math}`\bar{K}_s` is the average number of sets of traits in each subpopulation.