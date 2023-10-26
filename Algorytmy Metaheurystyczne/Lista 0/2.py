import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import sys

#-----------------TWORZENIE GRAFU----------------
with open(sys.argv[1], 'r') as file:
    G = nx.Graph()
    for line in file:
        words = line.split()
        if words[0] == 'DIMENSION':
            num_vertices = words[2]
        if words[0].isnumeric():
            G.add_edge(words[0], words[1], weight = words[2])

print(G)

for i, j in G.edges():
    print(i, "->", j, ": ", G[i][j]['weight'])

'''

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