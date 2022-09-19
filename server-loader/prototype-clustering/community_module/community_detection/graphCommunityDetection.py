# Authors: Jose Luis Jorro-Aragoneses

import networkx as nx
from networkx.algorithms import community
import markov_clustering as mc

ALGORITHMS = ['Markov', 'Greedy']

class GraphCommunityDetection:

    def __init__(self, graph):
        """Construct of GraphCommunityDetection objects

        Parameters
        ----------
        graph : nx.Graph
            Graph object where nodes are elements to search communities and
            edges are the relationships between nodes in graph.
        """
        self.graph = graph

    def calculate_communities(self, algorithm):
        """Method to calculate the communities of elements from graph.

        Parameters
        ----------
        algorithm : str
            Algorithm used to calculate the communities contained in
            a graph.

        Returns
        -------
        dict
            Dictionary with all elements and its corresponding community.
        """

        if algorithm == 'Markov':

            # Get adjacency matrix of graph
            A = nx.to_numpy_matrix(self.graph)

            # Apply Markov Clustering algorithm
            result = mc.run_mcl(A)
            clusters = mc.get_clusters(result)

            # Assign to each node its community id
            ids_communities = {}
            for i in range(len(clusters)):
                for node in clusters[i]:
                    ids_communities[node] = i
        
        if algorithm == 'Greedy':
            # Apply Markov Clustering algorithm
            communities_greedy = community.greedy_modularity_communities(self.graph)

            # Assign to each node its community id
            ids_communities = {}
            for i in range(len(communities_greedy)):
                for node in communities_greedy[i]:
                    ids_communities[node] = i

        return ids_communities