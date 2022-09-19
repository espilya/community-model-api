# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarity import Similarity


HECHT_BELIEFS_R = ['ANatPridePro','BReligousPro','CRealisticPro','DExtremistNeg','EReligousNeg','FRealisticNeg']


class HechtBeliefRSimilarity(Similarity):

        
    def beliefRDistance(self,beliefA,beliefB):
        # Special case: dont know
        if (beliefA == 'DK' and beliefB == 'DK'):
            return 0
        elif (beliefA == 'DK' or beliefB == 'DK'):
            return 0.5
    
    
    
        # Get index in belief values array
        indexA = HECHT_BELIEFS_R.index(beliefA)
        indexB = HECHT_BELIEFS_R.index(beliefB)

        if indexB > indexA:
            indexA, indexB = indexB, indexA
        
        # Category they belong to (pro - 0, against - 1)
        indexA3 = math.floor(indexA / 3)
        indexB3 = math.floor(indexB / 3)
        
        # Index inside the categories pro,against
        indexA2 = indexA % 3
        indexB2 = indexB % 3
        
        # Calculating distance
        # If they are in the same category: distance = index2 difference * 0.1
        # If they are in different categories: distance = 1 - index2 difference * 0.1
        
        # Example: BReligousPro and EReligousNeg are opposite. Different opinions based on same thinking process.
        # 2) ANatPridePro & BReligousPro are based on emotions, so they are closer than ANatPridePro and CRealisticPro since the latest one is based on cold logic.
        # 3) ANatPridePro is closer to FRealisticNeg because they are based on different thinking process
        
        # range (0-1)
        categoryDistance = indexA3 - indexB3
        
        # range (0-2)
        indexDistance = max(indexA2 - indexB2,indexB2 - indexA2)
        
        # Final distance
        distance = indexDistance * 0.2
        if (categoryDistance > 0):
            distance = 1 - distance
        
        return distance
        

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
        
        beliefA = self.data.loc[elemA]['beleifR']
        beliefB = self.data.loc[elemB]['beleifR']
        
        return self.beliefRDistance(beliefA,beliefB)
