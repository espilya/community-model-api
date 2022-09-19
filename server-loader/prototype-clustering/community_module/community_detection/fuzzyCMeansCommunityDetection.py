from fcmeans import FCM

class FuzzyCMeansCommunityDetection:

    def __init__(self, data):
        """Construct of opticsCommunityDetection.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data

    def calculate_communities(self, metric, n_clusters=5, max_iter=150, m=2.0, error=1e-5):
        """Method to calculate the communities of elements from data.

                Parameters
                ----------
                metric :
                    distanceMatrix
                n_clusters : int, optional
                    The number of clusters to form as well as the number
                max_iter : int, optional
                    Maximum number of iterations of the fuzzy C-means
                m : float, optional
                    Degree of fuzziness
                error : float, optional
                    Relative tolerance with regards to Frobenius norm of

                Returns
                -------
                dict
                    Dictionary with all elements and its corresponding community.
        """
        fcm = FCM(n_clusters=n_clusters, max_iter=max_iter, m=m, error=error)
        fcm.fit(metric)

        labels = fcm.predict(metric)
        ids_communities = {}
        for i in range(len(self.data.index)):
            ids_communities[self.data.index[i]] = labels[i]
        return ids_communities
