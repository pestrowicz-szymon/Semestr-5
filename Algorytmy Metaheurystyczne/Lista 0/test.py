import networkx as nx
import random
import matplotlib.pyplot as plt

G_1 = nx.Graph()
tempedgelist =  [[0, 2], [0, 3], [1, 2], [1, 4], [5, 3]]
G_1.add_edges_from(tempedgelist)

n_nodes = 6
pos = {i:(random.randint(0,50),random.randint(0,100)) for i in range(n_nodes)}
nx.draw(G_1, pos)
plt.show()