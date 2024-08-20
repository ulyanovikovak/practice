import networkx as nx
import pandas as pd
import numpy as np
from networkx.convert_matrix import to_numpy_array
import matplotlib.pyplot as plt

from networkx.convert_matrix import to_numpy_array

def main():
    data = pd.read_csv("SWOW-EN_R123.csv", sep='\t')
    G = nx.DiGraph()
    for index, row in data.iterrows():
        cue = row['cue']
        response = row['response']
        strength = row['R123.Strength']
        if float(strength) < 0.01:
            continue
        G.add_edge(cue, response, weight=strength)

    # Запись графа в файл GraphML
    nx.write_graphml(G, "threshold_SNOW-EN_R123.graphml")

    print( G.number_of_nodes())




if __name__ == '__main__':
    main()









