import networkx as nx
from random import choice
from random import randint
import random
from epydemic import *



class SIR(CompartmentedModel):
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    REMOVED = 'R'
    DEAD = 'D'

    P_INFECTED = 'pInfected'
    P_INFECT = 'pInfect'
    P_REMOVE = 'pRemove'
    SI = 'SI'

    def build(self, params):
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)
        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)

        self.trackNodesInCompartment(self.INFECTED)
        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)

    def infect(self, t, e):
        (u, v) = e
        self.changeCompartment(u, self.INFECTED)
        self.markOccupied(e, t)

    def remove(self, t, n):
        self.changeCompartment(n, self.REMOVED)

def rand_transmission():
    # function to vary transmission probability
    return 0.01

def main():
    param = dict()
    param[SIR.P_INFECT] = 0.000025 # initial infected population based on karnataka data
    param[SIR.P_REMOVE] = 0.5
    param[SIR.P_INFECTED] = rand_transmission()

    n = 10 ** 3  # total population
    p = 0.05
    G = nx.erdos_renyi_graph(n, p)

    model = SIR() # initialize the simple model
    sim = SynchronousDynamics(model, G) #set up stochastic spread model
    result = sim.set(param).run() #run on our simple parameters

    print(result)



main()
