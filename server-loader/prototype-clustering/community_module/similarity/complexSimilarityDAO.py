# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarityDAO import SimilarityDAO


HECHT_BELIEFS_R = ['ANatPridePro','BReligousPro','CRealisticPro','DExtremistNeg','EReligousNeg','FRealisticNeg']

class ComplexSimilarityDAO(SimilarityDAO):

    def __init__(self,dao,similarityDict):
        """Construct of Similarity objects.

        Parameters
        ----------
        dao : dao to obtain data from database
        similarityDict: dictionary
            Dictionary with keys (similarity measure classes) and values (weight of that similarity measure)
        
        """
        super().__init__(dao)
        
        self.similarityDict = {}
        for similarity,weight in similarityDict.items():
            similarityMeasure = similarity(dao)
            self.similarityDict[similarityMeasure] = weight
        
        """
        hecht_beliefR_df = self.data
        hecht_beliefR_df2 = hecht_beliefR_df.copy()
        hecht_beliefR_df3 = hecht_beliefR_df2.dropna()
        
        hecht_beliefR_pivot_df = pd.pivot_table(hecht_beliefR_df3, columns=['beleifR','DemographicReligous'], index='user', fill_value=np.NaN, aggfunc=lambda x: x)
        self.data = hecht_beliefR_pivot_dfç
        """
        
        """
        df = self.data.copy()
        df = df.set_index('user')
        self.data = df.copy()
        """
        
        #print(self.data)
        
        
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
        complexDistance = 0
        complexWeight = 0
        for similarity,weight in self.similarityDict.items():
            simDistance = similarity.distance(elemA,elemB) 
            simDistance2 = simDistance * weight
            
            complexDistance += simDistance2
            complexWeight = complexWeight + weight 
            
            """
            
            print("\n")
            print(similarity)
            print("Similarity Distance: " + str(simDistance))
            print("Similarity Weight: " + str(weight))
            print("Similarity Distance (weight): " + str(simDistance2))
            print("Total distance: " + str(complexDistance))
            print("Total weight: " + str(complexWeight))
            print("\n")
            """
            
            """
            print("\n")
            print(similarity)
            print(weight)
            print("\n")
            """
        
        # Calculating final distance
        complexDistance = complexDistance / complexWeight
        #print("Final distance: " + str(complexDistance))
        
        
        return complexDistance
        
    def similarity(self,elemA, elemB):
        """Method to obtain the similarity between two element.

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
        return 1 - self.distance(elemA, elemB, numEmotions) # ¿No debería ser 1 / distancia?

        