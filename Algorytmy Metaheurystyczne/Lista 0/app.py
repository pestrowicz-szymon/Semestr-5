import networkx as nx
import random
import matplotlib.pyplot as plt
import sys
import math

def distance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

files = ["xqf131.tsp", "xqg237.tsp", "pma343.tsp", "pka379.tsp", "bcl380.tsp", "pbl395.tsp", "pbk411.tsp", "pbn423.tsp", "pbm436.tsp", "xql662.tsp"]
for file in files:
    print(file)
    #-----------------TWORZENIE GRAFU----------------
    G = nx.Graph()
    with open(file, 'r') as file:
        G = nx.Graph()
        data = []
        for line in file:
            words = line.split()
            if words[0] == 'DIMENSION':
                num_vertices = int(words[2])
            if words[0].isnumeric():
                data.append((int(words[0])-1, int(words[1]), int(words[2])))

    pos = {i:(data[i][1],data[i][2]) for i in range(num_vertices)}

    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            G.add_edge(i, j, weight=distance(data[i][1], data[i][2], data[j][1], data[j][2]))

    # Algorytm Kruskala do wyznaczenia MST
    mst = nx.minimum_spanning_tree(G)

    # Obliczanie wagi MST
    mst_weight = sum(mst[i][j]['weight'] for i, j in mst.edges())

    #for i, j in mst.edges():
    #    print(i, "->", j, ": ", mst[i][j]['weight'])

    # Wypisywanie wagi MST na terminalu
    print("Waga MST:", mst_weight)

    #-----------------ALGORYTM DFS----------------
    visited = [False] * num_vertices
    visited_counter = 0
    dfs_path = []
    starting_point = 0

    def DFSUtil(v, visited_counter):
        visited[v] = True
        visited_counter += 1
        dfs_path.append(v)
        #print(v)
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
    print("WAGA DFS: ", dfs_sum)
    print("DFS/MST:", dfs_sum/mst_weight)
    print()

    #nx.draw(G, pos)
    #plt.show()
