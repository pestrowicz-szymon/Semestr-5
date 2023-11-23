import networkx as nx
import math
import matplotlib.pyplot as plt
import random

def distance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def DFSUtil(v, visited_counter):
    visited[v] = True
    visited_counter += 1
    dfs_path.append(v)
    if visited_counter != num_vertices:
        min_weight = math.inf
        for neighbour in G.neighbors(v):
            if min_weight > G.get_edge_data(v, neighbour)['weight'] and not visited[neighbour]:
                min_weight = G.get_edge_data(v, neighbour)['weight']
                closest_vertex = neighbour    
        DFSUtil(closest_vertex, visited_counter)
    
def DFS(v, visited_counter):
    DFSUtil(v, visited_counter)

def swap(tablica, indeks1, indeks2):
    tablica[indeks1], tablica[indeks2] = tablica[indeks2], tablica[indeks1]

def LocalSearch(path, dfs_score):
    return LocalSearchUtil(path, dfs_score, len(path), 0)
    
def LocalSearchUtil(original_path, original_best_score, path_length, number_of_steps):
    path_copies = [original_path.copy() for _ in range(4*len(original_path))]
    current_best = original_best_score
    current_best_path = original_path
    for j in range(4*path_length):
        if math.floor(j/path_length) == 0:
            swap(path_copies[j], j, (j+1)%path_length)
        elif math.floor(j/path_length) == 1:
            swap(path_copies[j], j%path_length, (j+2)%path_length)
        elif math.floor(j/path_length) == 2:
            swap(path_copies[j], j%path_length, (j+3)%path_length)
            swap(path_copies[j], (j+1)%path_length, (j+2)%path_length)
        elif math.floor(j/path_length) == 3:
            swap(path_copies[j], j%path_length, (j+4)%path_length)
            swap(path_copies[j], (j+1)%path_length, (j+3)%path_length)
        current_result = sum(G[path_copies[j][i]][path_copies[j][(i+1)%path_length]]['weight'] for i in range(path_length))
        if current_result < current_best:
            current_best = current_result
            current_best_path = path_copies[j]
    if current_best < original_best_score:
        return LocalSearchUtil(current_best_path, current_best, path_length, number_of_steps+1)
    return original_path, number_of_steps


files = ["xqf131.tsp", "xqg237.tsp", "pma343.tsp", "pka379.tsp", "bcl380.tsp", "pbl395.tsp", "pbk411.tsp", "pbn423.tsp", "pbm436.tsp", "xql662.tsp"]
for file in files:
    print(file)
    #-----------------TWORZENIE GRAFU----------------
    G = nx.Graph()
    dfs_g = nx.Graph()
    with open('data/'+file, 'r') as file:
        data = []
        for line in file:
            words = line.split()
            if words[0] == 'DIMENSION':
                num_vertices = int(words[2])
            if words[0].isnumeric():
                data.append((int(words[0])-1, int(words[1]), int(words[2])))
                dfs_g.add_node(int(words[0])-1, pos=(int(words[1]), int(words[2])))

    pos = {i:(data[i][1],data[i][2]) for i in range(num_vertices)}


    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            G.add_edge(i, j, weight=distance(data[i][1], data[i][2], data[j][1], data[j][2]))

    #-----------------OBLICZANIE MST----------------
    mst = nx.minimum_spanning_tree(G)
    mst_weight = sum(mst[i][j]['weight'] for i, j in mst.edges())
    print("Waga MST:", mst_weight)
    #filename = "graph/mst" + file.name[5:-4] + ".png"
    #nx.draw(mst, pos, node_size=20, node_color='red')
    #plt.savefig(filename)
    #plt.clf()

    local_sum_of_all = 0
    dfs_sum_of_all = 0
    sum_of_steps = 0
    best_result = math.inf

    #-----------------OBLICZANIE DFS----------------
    for n in range(math.ceil(math.sqrt(num_vertices))):
        visited = [False] * num_vertices
        visited_counter = 0
        dfs_path = []
        starting_point = random.randint(0, num_vertices)

        DFS(starting_point, visited_counter)
        dfs_sum = sum(G[dfs_path[i]][dfs_path[i+1]]['weight'] for i in range(num_vertices-1)) + G[dfs_path[num_vertices-1]][dfs_path[0]]['weight']

        for i in range(len(dfs_path)):
            dfs_g.add_edge(dfs_path[i], dfs_path[(i+1)%len(dfs_path)]) 
        
        #print(dfs_path)

        #print("WAGA DFS:", dfs_sum)
        dfs_sum_of_all += dfs_sum
        #filename = "graph/dfs" + file.name[5:-4] + "_" + str(n) + ".png"
        #nx.draw(dfs_g, pos, node_size=20, node_color='red')
        #plt.savefig(filename)
        #plt.clf()
        #dfs_g.remove_edges_from(list(dfs_g.edges()))

        
        local_path = LocalSearch(dfs_path, dfs_sum)[0]
        sum_of_steps += LocalSearch(dfs_path, dfs_sum)[1]
        local_sum = sum(G[local_path[i]][local_path[i+1]]['weight'] for i in range(num_vertices-1)) + G[local_path[num_vertices-1]][local_path[0]]['weight']
        local_sum_of_all += local_sum
        if local_sum < best_result:
            best_result = local_sum
        #print("WAGA LOCAL:", local_sum)
        for i in range(len(local_path)):
            dfs_g.add_edge(local_path[i], local_path[(i+1)%len(local_path)]) 
        #filename = "graph/local" + file.name[5:-4] + "_" + str(n) + ".png"
        #nx.draw(dfs_g, pos, node_size=20, node_color='red')
        #plt.savefig(filename)
        #plt.clf()
        #dfs_g.remove_edges_from(list(dfs_g.edges()))
        print(n,"/",math.ceil(math.sqrt(num_vertices)))
    
    print("best found local: ", best_result)
    print("average steps: ", sum_of_steps/math.ceil(math.sqrt(num_vertices)))
    print("average local result:", local_sum_of_all/math.ceil(math.sqrt(num_vertices)))
    print("average dfs result:", dfs_sum_of_all/math.ceil(math.sqrt(num_vertices)))
    print()