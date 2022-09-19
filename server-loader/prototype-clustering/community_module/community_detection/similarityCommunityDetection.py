# Authors: Jose Luis Jorro-Aragoneses

from math import nan
import numpy as np
from sklearn.cluster import AgglomerativeClustering

SKLEARN_METRICS = ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']

class SimilarityCommunityDetection:

    def __init__(self, data):
        """Construct of SimilariyCommunityDetection objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data

    def calculate_communities(self, metric='euclidean', n_clusters=2):
        """Method to calculate the communities of elements from data.

        Parameters
        ----------
        metric : str or Class, optional
            Metric used to calculate the distance between elements, by default 'euclidean'. It is
            possible to use a class with the same properties of Similarity.
        n_clusters : int, optional
            Number of clusters (communities) to search, by default 2

        Returns
        -------
        dict
            Dictionary with all elements and its corresponding community.
        """
        if metric in SKLEARN_METRICS:
            alg = AgglomerativeClustering(n_clusters=n_clusters, affinity=metric, linkage='average')
            result = alg.fit_predict(self.data.values)
        else:
            alg = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed', linkage='average')

            #TODO: Llamar a función de similitud y crear la matriz de distancias
            if callable(metric):
                sim = metric(self.data)
                distances = sim.matrix_distance()
                result = alg.fit_predict(distances)
            
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        ids_communities = {}
        for i in range(len(self.data.index)):
            ids_communities[self.data.index[i]] = result[i]

        return ids_communities