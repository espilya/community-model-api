# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarityDAO import SimilarityDAO


HECHT_BELIEFS_J = ['NotTraitor','CantJudge','Traitor']


class HechtBeliefJSimilarityDAO(SimilarityDAO):

    def distance(self,elemA, elemB):
        #print(self.data)
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
        
        valueA = self.data.loc[elemA]['beliefJ']
        valueB = self.data.loc[elemB]['beliefJ']
        
        indexA = HECHT_BELIEFS_J.index(valueA)
        indexB = HECHT_BELIEFS_J.index(valueB)
        
        return (abs(indexA - indexB)) / (len(HECHT_BELIEFS_J) - 1)