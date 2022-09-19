# Authors: Jose Angel Sanchez

from math import nan
import numpy as np
#from sklearn_extra.cluster import KMedoids

from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


# https://python-kmedoids.readthedocs.io/en/latest/index.html

class KmedoidsCommunityDetectionDistanceMatrix:

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
            #kmedoids_instance = kmedoids(distanceMatrix, initial_medoids, data_type='distance_matrix')
        
            # setting distance_threshold=0 ensures we compute the full tree.
            #alg = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed', linkage='average',compute_distances=True)
            
            #alg = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed', linkage='average')
            #result = alg.fit_predict(metric)
            
            #kmedoids = KMedoids(metric='precomputed',method='pam', n_clusters=n_clusters, init='k-medoids++')
            #kmedoids.fit(self.data)
            
            distanceMatrix = metric
            
            initial_medoids = kmeans_plusplus_initializer(distanceMatrix, n_clusters).initialize(return_index=True)
            print("\n")
            print("initial medoids")
            print("\n")
            print(initial_medoids)
            print("\n")
            
            # create K-Medoids algorithm for processing distance matrix instead of points
            kmedoids_instance = kmedoids(distanceMatrix, initial_medoids, data_type='distance_matrix')
            
            # run cluster analysis and obtain results
            result = kmedoids_instance.process()
            
            # Get clusters and medoids
            clusters = kmedoids_instance.get_clusters()
            medoids = kmedoids_instance.get_medoids()
            
            print("\n")
            print("clusters: ")
            print(clusters)
                
        
        """
        print(kmedoids.labels_)
        result = kmedoids.labels_

            
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        ids_communities = {}
        for i in range(len(self.data.index)):
            ids_communities[self.data.index[i]] = result[i]
        """
        
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        ids_communities = {}
        counter = 0
        for i in range(len(clusters)):
            counter += len(clusters[i])
            for j in range(len(clusters[i])):
                row = clusters[i][j]
                ids_communities[self.data.index[row]] = i
        
        ids_communities = dict(sorted(ids_communities.items(), key=lambda item:item[0]))
        
        
        print("\n")
        print("ids_communities")
        print("\n")
        print(ids_communities)
        print("\n")
        return ids_communities
    
    def get_distances(self,X,model,mode='l2'):
        distances = []
        weights = []
        children=model.children_
        dims = (X.shape[1],1)
        distCache = {}
        weightCache = {}
        for childs in children:
            c1 = X[childs[0]].reshape(dims)
            c2 = X[childs[1]].reshape(dims)
            c1Dist = 0
            c1W = 1
            c2Dist = 0
            c2W = 1
            if childs[0] in distCache.keys():
                c1Dist = distCache[childs[0]]
                c1W = weightCache[childs[0]]
            if childs[1] in distCache.keys():
                c2Dist = distCache[childs[1]]
                c2W = weightCache[childs[1]]
            d = np.linalg.norm(c1-c2)
            cc = ((c1W*c1)+(c2W*c2))/(c1W+c2W)

            X = np.vstack((X,cc.T))

            newChild_id = X.shape[0]-1

            # How to deal with a higher level cluster merge with lower distance:
            if mode=='l2':  # Increase the higher level cluster size suing an l2 norm
                added_dist = (c1Dist**2+c2Dist**2)**0.5 
                dNew = (d**2 + added_dist**2)**0.5
            elif mode == 'max':  # If the previrous clusters had higher distance, use that one
                dNew = max(d,c1Dist,c2Dist)
            elif mode == 'actual':  # Plot the actual distance.
                dNew = d


            wNew = (c1W + c2W)
            distCache[newChild_id] = dNew
            weightCache[newChild_id] = wNew

            distances.append(dNew)
            weights.append( wNew)
        return distances, weights
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def communitiesDistance(self,model, **kwargs):
        # Create linkage matrix and then plot the dendrogram

        # create the counts of samples under each node
        counts = np.zeros(model.children_.shape[0])
        n_samples = len(model.labels_)
        for i, merge in enumerate(model.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        linkage_matrix = np.column_stack(
            [model.children_, model.distances_, counts]
        ).astype(float)
        
        print(linkage_matrix)
        
    
    def plot_dendrogram(self,model, **kwargs):
        # Create linkage matrix and then plot the dendrogram

        # create the counts of samples under each node
        counts = np.zeros(model.children_.shape[0])
        n_samples = len(model.labels_)
        for i, merge in enumerate(model.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        linkage_matrix = np.column_stack(
            [model.children_, model.distances_, counts]
        ).astype(float)

        # Plot the corresponding dendrogram
        dendrogram(linkage_matrix, **kwargs)
   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def communityCentroid(self, communityId=99999):
        print("hsd")
        clf = NearestCentroid()
        print("saaa")
        print(self)
        print(communityId)
        clf.fit(self.data.values, self.result)
        print(clf.centroids_)
        
    
    
    