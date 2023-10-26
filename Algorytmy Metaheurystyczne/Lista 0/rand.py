import networkx as nx
import math
import random

def distance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

files = ["xqf131.tsp", "xqg237.tsp", "pma343.tsp", "pka379.tsp", "bcl380.tsp", "pbl395.tsp", "pbk411.tsp", "pbn423.tsp", "pbm436.tsp", "xql662.tsp"]
for file in files:
    print(file)
    #-----------------TWORZENIE GRAFU----------------
    G = nx.Graph()
    with open('data/'+file, 'r') as file:
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

    random_results = []
    minimums_10_avg = 0
    minimums_50_avg = 0
    for i in range(1000):
        vertices = list(G.nodes())
        random.shuffle(vertices)
        vertices.append(vertices[0])
        sum = 0
        for j in range(num_vertices):
            sum += G[vertices[j]][vertices[j+1]]['weight']
        random_results.append(sum)
    for i in range(100):
        minimums_10_avg += min(random_results[i*10:(i+1)*10])
    for i in range(20):
        minimums_50_avg += min(random_results[i*50:(i+1)*50])
    print("Średnia z minimum dla każdych 10 kolejnych losowań: ", minimums_10_avg/100)
    print("Średnia z minimum dla każdych 50 kolejnych losowań: ", minimums_50_avg/20)
    print("Średnia z minimum dla 1000 losowań: ", min(random_results))
    print()
        
        
