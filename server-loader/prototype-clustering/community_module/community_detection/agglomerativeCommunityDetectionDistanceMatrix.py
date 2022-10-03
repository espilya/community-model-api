# Authors: José Ángel Sánchez Martín, Jose Luis Jorro-Aragoneses


from math import nan
import numpy as np
from sklearn.cluster import AgglomerativeClustering

SKLEARN_METRICS = ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']

class AgglomerativeCommunityDetectionDistanceMatrix:

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
        #if metric in SKLEARN_METRICS:
        if False:
            alg = AgglomerativeClustering(n_clusters=n_clusters, affinity=metric, linkage='average')
            result = alg.fit_predict(self.data.values)
        # Distance Matrix
        else:
            # setting distance_threshold=0 ensures we compute the full tree.
            alg = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed', linkage='average',compute_distances=True)
            
            #alg = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed', linkage='average')
            result = alg.fit_predict(metric)

        return result
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def communityCentroid(self, communityId=99999):
        print("hsd")
        clf = NearestCentroid()
        print("saaa")
        print(self)
        print(communityId)
        clf.fit(self.data.values, self.result)
        print(clf.centroids_)
        
    
    
    