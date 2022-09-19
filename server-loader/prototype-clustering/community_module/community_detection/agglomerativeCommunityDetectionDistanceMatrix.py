# Authors: Jose Luis Jorro-Aragoneses

from math import nan
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# To get centroids
from sklearn.neighbors import NearestCentroid

SKLEARN_METRICS = ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']

# https://stackoverflow.com/questions/46027996/why-doesnt-sklearn-cluster-agglomerativeclustering-give-us-the-distances-betwee
# https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html
# To get distances between clusters
from scipy.cluster.hierarchy import dendrogram

from sklearn.neighbors import NearestCentroid



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
        
        #print(result)
        """
        #TODO: Llamar a función de similitud y crear la matriz de distancias
        if callable(metric):
            sim = metric(self.data)
            distances = sim.matrix_distance()
            result = alg.fit_predict(distances)
        """               
                
            
        # Asignamos a cada elemento su cluster/comunidad correspondiente
        ids_communities = {}
        for i in range(len(self.data.index)):
            ids_communities[self.data.index[i]] = result[i]
        
        
        """
        #added now for testing
        self.result = result
        
        
        #https://stackoverflow.com/questions/56456572/how-to-get-agglomerative-clustering-centroid-in-python-scikit-learn        
        # try to find centroid
        #y_predict = clusterer.fit_predict(X)
        #...
        clf = NearestCentroid()
        clf.fit(metric, result)
        print(clf.centroids_)
        """
        
        """
        # get distances
        distance, weight = self.get_distances(metric,alg)
        linkage_matrix = np.column_stack([alg.children_, distance, weight]).astype(float)
        print(linkage_matrix)
        """
        
        """
        plt.figure(figsize=(20,10))
        dendrogram(linkage_matrix)
        plt.show()
        """
        
        """
        #print(alg.children_)
        print("\n")
        print(alg.distances_)
        print("\n")
        print(alg.labels_)
        print("a")
        
        
        print(len(ids_communities))
        print(len(alg.labels_))
        print(len(alg.children_))
        print(len(alg.distances_))
        
        # Get distance between clusters
        #self.communitiesDistance(alg)
        # plot the top three levels of the dendrogram
        #plot_dendrogram(model, truncate_mode="level", p=3)
        
        
        # plot the top three levels of the dendrogram
        self.plot_dendrogram(alg, truncate_mode="level", p=3)
        plt.xlabel("Number of points in node (or index of point if no parenthesis).")
        plt.show()
        """
        
        """
        print("\n")
        print("ids_communities")
        print("\n")
        print(ids_communities)
        print("\n")
        """
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
        
    
    
    