import networkx as nx
import matplotlib.pyplot as plt
import random
import math

#-----------------TWORZENIE GRAFU----------------
G = nx.Graph()
num_vertices = 10
for i in range(num_vertices):
    G.add_node(i)
for i in range(num_vertices):
    for j in range(i+1, num_vertices):
        weight = random.randint(1, 1000)
        G.add_edge(i, j, weight=weight)

#-----------------OBLICZANIE MST----------------
mst = nx.minimum_spanning_tree(G)
mst_weight = sum(mst[i][j]['weight'] for i, j in mst.edges())
print("Waga MST:", mst_weight)

#-----------------WYPISANIE KRAWEDZI----------------
print("All edges and weights: ")
for i, j in G.edges():
    print(i, "->", j, ": ", G[i][j]['weight'])
print("MST edges and weights: ")
for i, j in mst.edges():
    print(i, "->", j, ": ", mst[i][j]['weight'])


#-----------------ALGORYTM DFS WERSJA 1----------------
visited = [False] * num_vertices
visited_counter = 0
dfs_path = []
starting_point = 0

def DFSUtil(v, visited_counter):
    visited[v] = True
    visited_counter += 1
    dfs_path.append(v)
    print(v, end=" ")
    if visited_counter != num_vertices:
        min_weight = math.inf
        for neighbour in G.neighbors(v):
            if min_weight > G.get_edge_data(v, neighbour)['weight'] and not visited[neighbour]:
                min_weight = G.get_edge_data(v, neighbour)['weight']
                closest_vertex = neighbour    
        DFSUtil(closest_vertex, visited_counter)
    else:
        dfs_path.append(starting_point)
 
def DFS(v, visited_counter):
    DFSUtil(v, visited_counter)

DFS(starting_point, visited_counter)

dfs_sum = sum(G[dfs_path[i]][dfs_path[i+1]]['weight'] for i in range(num_vertices))
print()
print(dfs_sum)
'''

#-----------------ALGORYTM DFS WERSJA 2----------------
sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])

for edge in sorted_edges:
    print(f"Krawędź: {edge[0]} -> {edge[1]}, Waga: {edge[2]['weight']}")

tps_path = []
used = [0] * num_vertices

for edge in sorted_edges:
    if used[edge[0]] < 2 and used[edge[1]] < 2:
        tps_path.append(edge)
        used[edge[0]] += 1
        used[edge[1]] += 1

print(tps_path)
'''
