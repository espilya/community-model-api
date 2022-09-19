# Authors: José Ángel Sánchez Martín

from math import nan
import numpy as np

from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

class KmedoidsCommunityDetection:

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
        
        distanceMatrix = metric        
        
        # Initialize initial medoids using K-Means++ algorithm
        initial_medoids = kmeans_plusplus_initializer(distanceMatrix, n_clusters).initialize(return_index=True)
        initial_medoids = [1,3,5,7,9]
                
        # create K-Medoids algorithm for processing distance matrix instead of points
        kmedoids_instance = kmedoids(distanceMatrix, initial_medoids, data_type='distance_matrix')
         
        # run cluster analysis and obtain results
        result = kmedoids_instance.process()
        
        # Get clusters and medoids
        clusters = kmedoids_instance.get_clusters()
        medoids = kmedoids_instance.get_medoids()
        
        #print("\n\n")
        #print(clusters)
        #print(medoids)
        
        
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

    