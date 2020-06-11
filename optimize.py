import networkx
from epydemic import *
import networkx as nx
import matplotlib.pyplot as plt
from random import choice 
import random
import matplotlib.pyplot as plt
from random import choice 
import numpy as np
import random
import numpy as np
import numpy.random as rn
import seaborn as sns
from scipy import optimize 
from scipy.optimize import minimize 

data = [] # need to store an array of cumulative cases for a place here, let's work on scraping the data from the link you shared


def spread(p, t):
  current_time = 1
  currently_infected = set()
  not_infected = set()

  list_time = list()
  list_alive = list()
  list_dead = list()
  list_susceptible = list()
  list_infected = list()
  list_recovered = list()
  current_dead = 0
  current_recovered = 0
  current_infected = infected

  for u in G:
    if label[u][0] == "I":
      currently_infected.add(u)
    
  count_no_spread_days = 0

  current_susceptible = population - infected
  list_time.append(1)
  list_alive.append(population - current_dead)
  list_dead.append(0)
  list_susceptible.append(current_susceptible)
  list_infected.append(infected)
  list_recovered.append(0)

  while count_no_spread_days < 30:
    current_time += 1
    new_infections = set()
    for u in currently_infected:
      if label[u][0] == 'I':
        if (current_time - label[u][1]) > 27:
          if random.randint(0, 10) > 1:
            label[u] = ("R", current_time)
            current_recovered += 1
          else:
            label[u] = ("D", current_time)
            current_dead += 1
        else:
          for v in list(G.neighbors(u)):
            if label[v][0] == 'S' and G.edges[u,v]['weight'] < 2:
              label[v] = ("I", current_time)
              new_infections.add(v)
              current_infected += 1

  currently_infected = currently_infected.union(new_infections)
  if len(new_infections) == 0:
    count_no_spread_days += 1
  current_susceptible = population - current_infected
  list_time.append(current_time)
  list_alive.append(population - current_dead)
  list_dead.append(current_dead)
  list_susceptible.append(current_susceptible)
  list_infected.append(current_infected)
  list_recovered.append(current_recovered)

  return list_infected

def cost_thorough():
  #working on writing a more thorough cost function here to take into account more parameters from the spread, and a more thorough error function
  #for instance include list_recovered and others too

def cost(arr):
  p = arr[0]
  t = arr[1]
  result = spread(p, t)
  total = 0
  for i in range(len(result)): # make sure while training the size of data = the number of iterations the spread functions runs for
    total += ((data[i] - result[i])^2)
  return total

def optimize():
  init_guess = [0.05, 0.1]
  result = minimize(cost, init_guess)
  if(result.success):
    print(result.x)
  else:
    raise ValueError(result.message)
  
def main():
  optimize()

if __name__ == '__main__':
  main()
