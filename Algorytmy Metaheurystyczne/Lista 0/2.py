import networkx as nx
import matplotlib.pyplot as plt
import random

def dfs(graph, start, visited, path):
    visited[start] = True
    path.append(start)
    for neighbor in graph.neighbors(start):
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, path)

def cykl(path, mst):
    sum = 0
    for p in path:
        previous = p
        sum += mst[previous][p+1]
        print(mst[previous][p+1])
    return sum
        


# Tworzenie pustego grafu nieskierowanego
G = nx.Graph()

# Tworzenie 10 losowych wierzchołków
num_vertices = 10
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

# Wypisywanie wagi MST na terminalu
print("Waga MST:", mst_weight)

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

#plt.show()

# Tworzenie grafu nieskierowanego z MST
mst_graph = nx.Graph()
for u, v, data in mst.edges(data=True):
    weight = data['weight']
    mst_graph.add_edge(u, v, weight=weight)

# Wierzchołek początkowy (możesz wybrać dowolny)
start_node = 0

# Przeszukiwanie w głąb
visited = [False] * num_vertices
path = []
dfs(mst_graph, start_node, visited, path)

# Zamknięcie cyklu
path.append(start_node)

# Obliczanie wagi cyklu komiwojażera
#tsp_weight = sum(mst[u][v]['weight'] for u, v in path)
#print("Waga cyklu komiwojażera:", tsp_weight)
print(path)

print(cykl(path, mst))