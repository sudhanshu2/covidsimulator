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
from scipy.optimize import minimize_scalar
import ijson
import datetime
import requests 
import os 

with requests.get("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/", stream=True) as r:
  r.raise_for_status()
  with open("data.json", 'wb') as f:
    chunk_count = 0
    for chunk in r.iter_content(chunk_size=512): 
      chunk_count += 1
      f.write(chunk)

print("retrieved a JSON file of size " + str(os.stat("data.json").st_size / 1000000) + " MB in " + str(chunk_count) + " chunks")

cases_per_day = []
death_per_day = []
dates = []

cases = []
death = []

date_current = datetime.date.today()
case_count = 0
death_count = 0

with open("data.json", 'r') as covid_data:
  parser = ijson.parse(covid_data)
  for prefix, event, value in parser:
    if prefix == "records.item.dateRep":
      date_current = datetime.datetime.strptime(value, "%d/%m/%Y").date()
    if prefix == "records.item.cases":
      case_count = int(value)
    if prefix == "records.item.deaths":
      death_count = int(value)
    if prefix == "records.item.countriesAndTerritories" and value == "India":
      cases_per_day.append(case_count)
      death_per_day.append(death_count)
      dates.append(date_current)

cases_per_day.reverse()
death_per_day.reverse()
dates.reverse()

print(len(cases_per_day))
print(len(death_per_day))

cases.append(cases_per_day[0])
death.append(death_per_day[0])

for i in range(1, len(cases_per_day)):
  cases.append(cases_per_day[i] + cases[i - 1])
  death.append(death_per_day[i] + death[i - 1])


def spread(p, t):
  population = 1000
  susceptible = 0
  recovered = 0
  iterations = 30 
  infected=1
  
  print("right before creating the graph")
  G = nx.erdos_renyi_graph(population, p)
  print("created graph\n")
  for (u, v) in G.edges():
    G.edges[u,v]['weight'] = random.randint(0,100)

  label = {}
  count = 0
  for node in G:
    if (random.randint(0, 10) > 4) and count < infected:
      label[node] = ("I", 1)
      count = count + 1
    else:
      label[node] = ("S", 0)


  current_time = 1
  currently_infected = set()
  not_infected = set()

  list_time = list()
  list_alive = list()
  list_dead = list()
  list_susceptible = list()
  list_infected = list()
  list_recovered = list()
  list_cases_per_day = list()
  current_dead = 0
  current_recovered = 0
  current_infected = 1

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

  while count_no_spread_days <= 30:
    current_time += 1
    new_infections = set()
    cases_on_iteration = 0
    # new cases holds a count for the new cases for each
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
              cases_on_iteration += 1

    list_cases_per_day.append(cases_on_iteration)
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


def cost(arr):
  p = arr[0]
  t = arr[1]
  result = spread(p, t)
  data = cases[0:len(result)]
  total = 0
  print("lengths: ", len(data), len(result))
  for i in range(len(result)): # make sure while training the size of data = the number of iterations the spread functions runs for
    total += ((data[i] - result[i])**2)
  print("total: ", total)
  return total

def optimize():
  prange = ((0, 1), (0, 1))
  init_guess = [0.05, 0.1]
  res = minimize(cost, arr, bounds=prange)
  if(result.success):
    print(result.x)
  else:
    raise ValueError(result.message)

  
optimize()
