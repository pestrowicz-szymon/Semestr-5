import networkx as nx
import matplotlib.pyplot as plt
import random

# Tworzenie pustego grafu nieskierowanego
G = nx.Graph()

# Tworzenie 10 losowych wierzchołków
num_vertices = 6
for i in range(num_vertices):
    G.add_node(i)

# Dodawanie losowych krawędzi z losowymi wagami
for i in range(num_vertices):
    for j in range(i+1, num_vertices):
        weight = random.randint(1, 1000)  # Losowa waga od 1 do 1000
        G.add_edge(i, j, weight=weight)

# Algorytm Kruskala do wyznaczenia MST
mst = nx.minimum_spanning_tree(G)

# Obliczanie wagi MST
mst_weight = sum(mst[i][j]['weight'] for i, j in mst.edges())

for i, j in mst.edges():
    print(i, "->", j, ": ", mst[i][j]['weight'])

# Wypisywanie wagi MST na terminalu
print("Waga MST:", mst_weight)

"""
# Rysowanie grafu
pos = nx.spring_layout(G)  # Układ wierzchołków
edge_labels = {(i, j): G[i][j]['weight'] for i, j in G.edges()}
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
plt.show()
"""

# Rysowanie grafu
pos = nx.spring_layout(G)  # Układ wierzchołków
edge_labels = {(i, j): G[i][j]['weight'] for i, j in G.edges()}

# Tworzenie MST
mst_edge_labels = {(i, j): mst[i][j]['weight'] for i, j in mst.edges()}

# Rysowanie pierwotnego grafu
plt.figure(figsize=(12, 5))
plt.subplot(121)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
plt.axis('off')

# Rysowanie MST
plt.subplot(122)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels=mst_edge_labels, font_color='red')
nx.draw_networkx_edges(G, pos, edgelist=mst.edges(), edge_color='green', width=2)
plt.axis('off')

plt.show()