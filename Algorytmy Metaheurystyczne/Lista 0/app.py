import networkx as nx
import math
import matplotlib.pyplot as plt

def distance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

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

    #-----------------OBLICZANIE DFS----------------
    visited = [False] * num_vertices
    visited_counter = 0
    dfs_path = []
    starting_point = 0



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
        else:
            dfs_path.append(starting_point)
    
    def DFS(v, visited_counter):
        DFSUtil(v, visited_counter)

    DFS(starting_point, visited_counter)
    dfs_sum = sum(G[dfs_path[i]][dfs_path[i+1]]['weight'] for i in range(num_vertices))

    for i in range(len(dfs_path)-1):
        dfs_g.add_edge(dfs_path[i], dfs_path[i+1])

    #-----------------WYPISYWANIE WYNIKÓW----------------
    print("WAGA DFS: ", dfs_sum)
    print("DFS/MST:", dfs_sum/mst_weight)

    filename1 = "graph/mst" + file.name[5:-4] + ".png"
    filename2 = "graph/dfs" + file.name[5:-4] + ".png"
    print(file.name)
    nx.draw(mst, pos, node_size=20, node_color='red')
    plt.axis('off')
    plt.savefig(filename1)
    nx.draw(dfs_g, pos, node_size=20, node_color='red')
    plt.axis('off')
    plt.savefig(filename2)

    print()