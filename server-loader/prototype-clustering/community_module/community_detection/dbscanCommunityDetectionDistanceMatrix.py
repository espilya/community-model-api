# Authors: José Ángel Sánchez Martín

from math import nan
import numpy as np

from sklearn.cluster import DBSCAN

class DbscanCommunityDetectionDistanceMatrix:

    def __init__(self, data):
        """Construct of SimilariyCommunityDetection objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data
        
       # print(self.data)

    def calculate_communities(self, metric='euclidean', n_clusters=2):
        """Method to calculate the communities of elements from data.

        Parameters
        ----------
        metric : str or Class, optional
            Metric used to calculate the distance between elements, by default 'euclidean'. It is
            possible to use a class with the same properties of Similarity.
            
            Metric is a distance matrix in this case
        n_clusters : int, optional
            Number of clusters (communities) to search, by default 2

        Returns
        -------
        dict
            Dictionary with all elements and its corresponding community.
        """
        
        # run dbscan
        distanceMatrix = metric 
        
        # https://github.com/scikit-learn/scikit-learn/issues/6787
        #distanceMatrix = sklearn.metrics.pairwise.euclidean_distances(self.data,self.data)
        
        print(distanceMatrix)
        #print(self.data)

        #dbscan = DBSCAN(eps=0.1, min_samples=7, metric='precomputed')
        dbscan = DBSCAN( metric='precomputed' , eps = .1, min_samples = 7)
        #dbscan.fit(distanceMatrix)
        dbscan.fit(distanceMatrix)
        
        print("ehet")
        
        
        # Get clusters
        clusters = dbscan.labels_
        
        print(clusters)
        print(len(clusters))
        print(len(self.data))
                
        
        
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        ids_communities = {}
        counter = 0
        for i in range(len(clusters)):
            counter += len(clusters[i])
            for j in range(len(clusters[i])):
                row = clusters[i][j]
                ids_communities[self.data.index[row]] = i
        
        ids_communities = dict(sorted(ids_communities.items(), key=lambda item:item[0]))

        print("\n\n")
        print(ids_communities)
        print("\n\n")

        
        return ids_communities

    