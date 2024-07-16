# Coding metapopulations in Python

> Author: Matteo Tomasini
>
> Date started: 25 Jun 2024

## Motivation

Existing packages in Python for agent-based modelling (ABM), such as [Mesa](https://mesa.readthedocs.io/en/stable/), provide great tooling for ABM with single agents interacting on a grid - where a single agent or multiple agents can be at the same time in the same node. This is what is sometimes called in biology "Individual-based modelling", where the processes that affect individuals are in focus. Within this framework it is sometimes difficult to work with a focus on the subpopulation in which an individual is found - that is using "Population-based modelling". This is because most tools that come out of the box in such frameworks are based on the individual agents in the model. While it is possible to adapt them to work with metapopulations, I find it easier and faster to create my own library for such models.

Currently, the models that I want to implement have a need for a structure where individuals can move between subpopulations (demes) and interact, but the form of this interaction is not clear. Ideally, I will set up a system for which the form of the interaction can be supplied at the moment where the population is generated.

## Documentation

The documentation is hosted on [Matteo Tomasini's personal webpage](https://mtomasini.github.io/MetapopulationsPython).
