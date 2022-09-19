# Authors: José Ángel Sánchez Martín
import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarityDAO import SimilarityDAO


HECHT_POLITICS = ['VL','L','C','R','VR','DK']

class HechtDemographicPoliticsSimilarityDAO(SimilarityDAO):

        
    def distance(self,elemA, elemB):
        """Method to obtain the distance between two element.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Distance between the two elements.
        """        
        valueA = self.data.loc[elemA]['DemographicPolitics']
        valueB = self.data.loc[elemB]['DemographicPolitics']
        
        indexA = HECHT_POLITICS.index(valueA)
        indexB = HECHT_POLITICS.index(valueB)
        
        if (indexA == 5):
            if (indexB == 5):
                return 0
            else:
                return 1
        
        return (abs(indexA - indexB)) / (len(HECHT_POLITICS) - 2)
       
        