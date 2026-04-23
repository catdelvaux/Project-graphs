import pandas as pd
import matplotlib.pyplot as plt

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

    return sum(degrees.values)/len(degrees)

def number_of_bridges(df):
    """
    Returns the number of bridges in the graph
    """
    return 0

def number_of_local_bridges(df):
    """
    Returns the number of local bridges in the graph
    """
    return 0

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

histogram(df)