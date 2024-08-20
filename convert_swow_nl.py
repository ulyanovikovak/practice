import networkx as nx
import pandas as pd


def get_edges(data: pd.DataFrame):
    # Melt the DataFrame to long form
    edges = data.melt(id_vars='cue', value_vars=['asso1', 'asso2', 'asso3'], value_name='asso')

    # Create a new DataFrame with the edges and their counts
    edges = edges.groupby(['cue', 'asso']).size().reset_index(name='count')

    # Calculate sum for every cue
    total_count = edges.groupby('cue')['count'].transform('sum')

    # Calculate the normalized weight for each edge
    edges['weight'] = edges['count'] / total_count
    # Drop extra column
    edges = edges.drop(columns='count')

    # Convert the edges DataFrame to a list of tuples
    edges = list(edges.itertuples(index=False, name=None))

    return edges


def main():
    data = pd.read_csv("swow-nl.csv", sep=';')
    g = nx.DiGraph()
    # Get all unique words
    nodes = set(data['cue']).union(set(data['asso1'])).union(set(data['asso2'])).union(set(data['asso3']))
    g.add_nodes_from(nodes)
    # Get all edges with correct edge weights
    edges = get_edges(data)
    g.add_weighted_edges_from(edges)

    nx.write_graphml(g, "dutch_main.graphml")
    print("Граф успешно записан в файл dutch_main.graphml")


if __name__ == '__main__':
    main()
