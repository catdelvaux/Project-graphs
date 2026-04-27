import pandas as pd
import matplotlib.pyplot as plt


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def score(df, station):
    """
    Returns the score (as defined in the project statement) of a node named `station` in the graph
    """
    graph = build_graph(df)
    degrees = build_degrees(df)
    
    total = 0
    for i, dni in graph[station]:
        inner = 0
        for j, dij in graph[i]:
            if j != station:
                inner += degrees[j]*dij
        total += (degrees[i]/dni) * inner

    return degrees[station]*total

def gain_from_split(df, station_a, station_b):
    """
    Returns the gain (criterion defined above) from splitting the edge station_a - station_b.
    """
    return 0

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

def build_degrees(df):
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

    return degrees

#for the report
"""
graph = build_graph(df)
scores = {}
for station in graph:
    scores[station] = score(df, station)

sorted_stations = sorted(scores, key=scores.get, reverse=True)
print("Top 5:", [(s, scores[s]) for s in sorted_stations[:5]])
print("Bottom 5:", [(s, scores[s]) for s in sorted_stations[-5:]])

plt.hist(list(scores.values()), bins=50)
plt.xlabel("Score")
plt.ylabel("Number of stations")
plt.title("Score distribution")
plt.show()
"""