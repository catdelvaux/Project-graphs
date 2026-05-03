import pandas as pd
import heapq
import matplotlib.pyplot as plt


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def betweenness_centrality(df, station):
    """
    Returns the betweenness centrality score of a node named `station` in the graph
    """
    graph = build_graph(df)
    count = 0

    for source in graph:
        distances, prev = dijkstra(source, graph)
        for destination in graph:
            if destination != source:
                current = destination
                while current != source:
                    if current is None:
                        break
                    if current != destination:
                        if current == station:
                            count += 1
                    current = prev[current]

    return count // 2

#helpers
def build_graph(df):
    graph={}

    for i, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]
        distance = float(row["distance_km"])

        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append((b, distance))
        graph[b].append((a, distance))
    
    return graph

def dijkstra(source, graph):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    prev = {node: None for node in graph}
    heap = [(0, source)]

    while heap:
        dist, node = heapq.heappop(heap)
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))
    
    return distances, prev


#print(betweenness_centrality(df, "Bruxelles-Midi_Brussel-Zuid"))

# compute all at once
def all_betweenness(df):
    graph = build_graph(df)
    counts = {node: 0 for node in graph}
    
    for source in graph:
        distances, prev = dijkstra(source, graph)
        for destination in graph:
            if destination != source:
                if destination > source:  
                    current = destination
                    while current != source:
                        if current is None:
                            break
                        if current != destination:
                            counts[current] += 1
                        current = prev[current]
        
    return counts

def find_max(df):
    counts = all_betweenness(df)
    max_station=max(counts, key=counts.get)
    max_score = counts[max_station]

    graph = build_graph(df)
    V = len(graph)
    normalization = (V-1) * (V-2) / 2
    normalized_score = max_score / normalization

    print(max_station, max_score, normalized_score)
    return counts

counts=find_max(df)
plt.hist(list(counts.values()), bins=50)
plt.xlabel("Betweenness centrality score")
plt.ylabel("Number of stations")
plt.title("Betweenness centrality distribution")
plt.show()