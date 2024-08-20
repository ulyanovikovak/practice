"""
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <graph id="G" edgedefault="directed">

    <!-- Определение узлов (вершин) -->
    <node id="n0">
      <data key="d0">Антихрист</data>
    </node>
    <node id="n1">
      <data key="d0">бог</data>
    </node>
    <!-- Добавьте другие узлы по аналогии -->

    <!-- Определение ребер (связей) с весами -->
    <edge id="e0" source="n0" target="n1">
      <data key="d1">1.0</data>
    </edge>
    <!-- Добавьте другие ребра по аналогии -->

  </graph>

   <!-- Определение ключей данных -->
  <key id="d0" for="node" attr.name="label" attr.type="string"/>
  <key id="d1" for="edge" attr.name="weight" attr.type="double"/>
</graphml>
"""

import csv
from collections import defaultdict
import networkx as nx
import pandas as pd


def get_edges(data: pd.DataFrame):
    df = data[['word', 'assoc', 'weight', 'mirror_weight', 'dir']]

    # Create a new DataFrame for forward edges
    edges = df[df['dir'].isin(['DIR', 'BIDIR'])][['word', 'assoc', 'weight']]
    edges.columns = ['source', 'target', 'weight']

    total_weight = edges.groupby('source')['weight'].transform('sum')

    # Calculate the normalized weight for each edge
    edges['weight'] = edges['weight'] / total_weight

    # Convert the edges DataFrame to a dictionary
    edges = edges.set_index(['source', 'target'])['weight'].to_dict()

    return edges


def main():
    data = pd.read_csv("assoc.csv", sep=';')
    g = nx.DiGraph()
    nodes = set(data['word']).union(set(data['assoc']))
    g.add_nodes_from(nodes)
    edges = get_edges(data)
    g.add_weighted_edges_from([(k[0], k[1], v) for k, v in edges.items()])

    # Запись графа в файл GraphML
    nx.write_graphml(g, "rus_main.graphml")

    # print("Граф успешно записан в файл rus_main.graphml")


if __name__ == '__main__':
    main()
