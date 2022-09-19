# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarity import Similarity
from sklearn.metrics.pairwise import cosine_similarity



HECHT_BELIEFS_E = ['Justify','Balanced','Oppose']


class cosineSimilarity(Similarity):

    def __init__(self,data):
        """Construct of Similarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements
        
        """
        self.data = data
    
    def matrix_distance(self):
        """Method to calculate the matrix of distance between all element included in data.

        Returns
        -------
        np.array
            Matrix that contains all similarity values.
        """
        users = self.data.index
        pairs = product(range(len(users)), repeat=2)

        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.distance(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist

        return matrix
    
        
        
        
        
        
        
        
        
        