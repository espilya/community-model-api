# Authors: Jose Luis Jorro-Aragoneses

from math import nan
import numpy as np

from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score

class KMeansCommunityDetection:

    def __init__(self, data):
        """Construct of SimilariyCommunityDetection objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element (numerical).
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
        n_clusters = self.calculateOptimalClusterNumber()
        km = KMeans(init='k-means++', n_clusters=n_clusters, random_state=43)
        km.fit(self.data.values)
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        labels = km.labels_
        centers = km.cluster_centers_
        #plot_clusters(users_interactions_values, labels, centers=None)   
        
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        ids_communities = {}
        for i in range(len(self.data.index)):
            ids_communities[self.data.index[i]] = labels[i]
        
        return ids_communities
        
        
        
    def calculateOptimalClusterNumber(self):
        K_MAX = 10
        score = np.zeros(K_MAX-2)
        davies_boulding = np.zeros(K_MAX-2)
        silhouette = np.zeros(K_MAX-2)
        for k in range(2, K_MAX): 
            km = KMeans(init='k-means++', n_clusters=k, random_state=43)
            km.fit(self.data.values)

        score[k-2] = -1 * km.score(self.data.values)
        davies_boulding[k-2] = davies_bouldin_score(self.data.values, km.labels_)
        silhouette[k-2] = silhouette_score(self.data.values, km.labels_)

        # Score (get elbow based on derivative)

        # Davies_boulding (min values)

        # Silhouette (max values)

        # Final result: choose the value that fits the three of them the most (if it is ambiguous, select based on davies-score-silhouette)

        optimalClusters = 5
        return optimalClusters
        
        
        
        
    
    
    