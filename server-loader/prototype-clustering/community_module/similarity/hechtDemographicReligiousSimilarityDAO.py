# Authors: José Ángel Sánchez Martín
import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarityDAO import SimilarityDAO


HECHT_RELIGIOUS = ['S','M','R','VR','H']


class HechtDemographicReligiousSimilarityDAO(SimilarityDAO):
        
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
        valueA = self.data.loc[elemA]['DemographicReligous']
        valueB = self.data.loc[elemB]['DemographicReligous']
        
        indexA = HECHT_RELIGIOUS.index(valueA)
        indexB = HECHT_RELIGIOUS.index(valueB)
        
        return (abs(indexA - indexB)) / (len(HECHT_RELIGIOUS) - 1)
       
        