import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigs
from networkx.convert_matrix import to_numpy_array


def get_limited_graph(name: str, limit: float):
    g = nx.read_graphml(name)
    edges_to_remove = [(u, v) for u, v, d in g.edges(data=True) if d['weight'] < limit]
    g.remove_edges_from(edges_to_remove)
    g.remove_nodes_from(list(nx.isolates(g)))

    return g


def main():
    names = ['en_r1']  # 'rus', 'en_r123', 'dutch'
    limits = [0.07, 0.08, 0.09, 0.1, 0.15]
    limits.reverse()
    for name in names:
        for limit in limits:
            print(name, limit)
            g = get_limited_graph(f'SNOW-EN_R1.graphml', limit)
            print("g", g.number_of_nodes(), g.number_of_edges())
            adj_matrix = nx.to_scipy_sparse_array(g)
            print("a")
            eigvals = eigs(adj_matrix, k=g.number_of_nodes() - 2, which='SM', return_eigenvectors=False)
            print(len(eigvals))
            print("e")
            np.savetxt(f'eigvals_with_limits_{name}_{limit}.csv', eigvals, delimiter=',')
        # g = nx.read_graphml(f"strong_graphml/{name}.graphml")
        # print("g")
        # adj_matrix = to_numpy_array(g)
        # adj_matrix = nx.to_scipy_sparse_array(g)
        # print("a")
        # eigvals = eigs(adj_matrix, k=300, which='SM', return_eigenvectors=False)
        # eigvals = np.linalg.eigvals(adj_matrix)
        # np.savetxt(f'strong_{name}_eigvals_300_sm.csv', eigvals, delimiter=',')
        # print("b")
        #
        # eigvals = eigs(adj_matrix, k=300, which='LM', return_eigenvectors=False)
        # eigvals = np.linalg.eigvals(adj_matrix)
        # np.savetxt(f'strong_{name}_eigvals_300_lm.csv', eigvals, delimiter=',')


if __name__ == '__main__':
    main()
