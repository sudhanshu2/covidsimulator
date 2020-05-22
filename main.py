import networkx
import matplotlib.pyplot as plt
from random import choice
from random import randint
import random

population = 10**3
infected = 100
susceptible = 0
recovered = 0
probability = 0.05

age_distribution = [35.3, 18.4, 27.6, 13.5, 4.8]
# the above array stores rough percentage composition by populatio of different age groups
# 0-14, 15-24, 25-44, 45-64, 64+
# we colour the nodes in the generated graph based on these values


def spread(G, size, labels):
	total_infected = 100
	tround = 1
	while True:
		tround += 1
		for v in list(G.nodes):
			if labels[v][0] == "R" or labels[v][0] == "D":
				continue
			# ignore the nodes that are either dead or recovered

			elif labels[v][0] == "S":
				neighbors = list(G.neighbors(v))
				for u in neighbors:  # for nodes that are still susceptible,
					if labels[u][0] == "I":
						if labels[u][1] in range(2, 10):
							if G[v][u]['weight'] > 0.3:
								labels[v] = ("I", tround)
								total_infected += 1
						else:
							if G[v][u]['weight'] > 0.6:
								labels[v] = ("I", tround)
								total_infected += 1

			else:
				# in this case the node is already infected or "I"
				if (tround - labels[v][1]) > 27:
				# if the person has been infected for more than an average of 4 weeks
				# then they either die or recovers.
				# a day here maps to one round of transmission
					if random.randint(0, 100) < 40:
						labels[v] = ("R", 0)
					else:
						labels[v] = ("D", 0)
				continue

		print(total_infected)

def colour_graph(G, size):
	colour_list = {"AD":0, "T":0, "YA":0, "MA":0, "O":0}
	# colour list stores the number of nodes coloured to be classified under each group
	# AD is adolescants(coloured green), T for teenagers(blue), YA for young adults(yellow), MA for middle-aged and O for old.
	# middle aged and older are coloured red
	colour_map = []
	for node in G:
		# we randomly colour each node to match the age distribution as closely as possible
		if ((100.0 * colour_list["AD"])/size) < age_distribution[0]:
			colour_map.append('green')
			colour_list["AD"] += 1
		elif ((100.0 * colour_list["T"])/size) < age_distribution[1]:
			colour_map.append('blue')
			colour_list["T"] += 1

		elif ((100.0 * colour_list["YA"])/size) < age_distribution[2]:
			colour_map.append('yellow')
			colour_list["YA"] += 1
			
		elif ((100.0 * colour_list["MA"])/size) < age_distribution[3]:
			colour_map.append('yellow')
			colour_list["MA"] += 1

		else:
			colour_map.append('red')
			colour_list["O"] += 1

	return colour_map

def create_graph(size, p):
	G = networkx.erdos_renyi_graph(size, p)
#	networkx.draw(G, with_labels=True) these two commented functions are to plot graphs themselves
	map = colour_graph(G, size)
#	networkx.draw(G, node_color=map, with_labels=True)
	count = 0
	labels = {}
	for node in G:
		if (random.randint(0, 1) == 1) and count < infected:
			labels[node] = ("I", 1)
			count = count + 1
		else:
			labels[node] = ("S", 0)

	for (u, v) in G.edges():
		num = random.randint(1, 100)
		G[u][v]['weight'] = (1.0 / num)

	spread(G, size, labels)

def main():
	create_graph(1000, 0.05)


#	plt.show()

main()
