import pandas as pd
import matplotlib.pyplot as plt
#mport sys
#sys.setrecursionlimit(100000)

INPUT_CSV = "data/total.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def average_degree(df):
    """
    Returns the average degree of the nodes in the graph
    """
    degrees={}

    for i, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]

        if a not in degrees:
            degrees[a] = 0
        if b not in degrees:
            degrees[b] = 0
        degrees[a] += 1
        degrees[b] += 1

    return sum(degrees.values())/len(degrees)

def number_of_bridges(df):
    """
    Returns the number of bridges in the graph
    """
    graph = build_graph(df)
    disc = {}
    low = {}
    visited = {}
    timer = [0]
    bridges = [0]

    for node in graph:
        if node not in visited:
            dfs_bridge(node, graph, disc, low, visited, timer, bridges)

    return bridges[0]

def number_of_local_bridges(df):
    """
    Returns the number of local bridges in the graph
    """
    graph = build_graph(df)
    local_bridges_count = 0

    for i, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]
        
        neighbors_a = set(graph[a])
        neighbors_b = set(graph[b])
    
        if len(neighbors_a & neighbors_b) == 0:
            local_bridges_count += 1

    return local_bridges_count

#histogram for report
def histogram(df):
    degrees={}

    for i, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]

        if a not in degrees:
            degrees[a] = 0
        if b not in degrees:
            degrees[b] = 0
        degrees[a] += 1
        degrees[b] += 1

    d = [0] * 11
    for i in degrees.values():
        if i <= 10:
            d[i] += 1

    plt.bar([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], d[1:11])
    plt.xlabel("Degree")
    plt.ylabel("Number of stations")
    plt.title("Degree distribution")
    plt.show()


#helpers
def dfs(node, graph, visited):
    visited[node] = True
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(neighbor, graph, visited)

def is_connected(graph):
    start = list(graph.keys())[0]

    visited = {node : False for node in graph}

    dfs(start, graph, visited)

    return all(visited.values())

def build_graph(df):
    graph={}

    for i, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]

        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        graph[b].append(a)
    
    return graph
"""
def dfs_bridgerec(node, parent, graph, disc, low, visited, timer, bridges):
    visited[node] = True
    disc[node] = timer[0]
    low[node] = timer[0]
    timer[0] += 1

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_bridge(neighbor, node, graph, disc, low, visited, timer, bridges)
            low[node] = min(low[node], low[neighbor])

            if low[neighbor] > disc[node]:
                bridges[0] += 1

        elif neighbor != parent:
            low[node] = min(low[node], disc[neighbor])
"""
def dfs_bridge(start, graph, disc, low, visited, timer, bridges):
    stack = [(start, None)]  # (node, parent)
    
    while stack:
        node, parent = stack[-1]
        
        if node not in visited:
            visited[node] = True
            disc[node] = timer[0]
            low[node] = timer[0]
            timer[0] += 1
        
        pushed = False
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append((neighbor, node))
                pushed = True
                break
            elif neighbor != parent:
                low[node] = min(low[node], disc[neighbor])
        
        if not pushed:
            stack.pop()
            if parent is not None:
                low[parent] = min(low[parent], low[node])
                if low[node] > disc[parent]:
                    bridges[0] += 1

#print(number_of_local_bridges(df))
#print(average_degree(df))
print(number_of_bridges(df))
#histogram(df)