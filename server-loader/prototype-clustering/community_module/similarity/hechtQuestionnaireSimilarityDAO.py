# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarityDAO import SimilarityDAO

from sklearn.metrics.pairwise import cosine_similarity



class HechtQuestionnaireSimilarityDAO(SimilarityDAO):

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
        
        
        #return cosine
        
        #cosine_similarity(self.data.loc[elemA], df.col2)
        
        
        #valueA = self.data.loc[elemA]['LQAOTPrepOpenBeleifsImportant','LQRHMSPrepHistUnderstandNews']
        #valueB = self.data.loc[elemB]['LQAOTPrepOpenBeleifsImportant','LQRHMSPrepHistUnderstandNews']
        
        df = self.data.loc[[elemA,elemB],['LQAOTPrepOpenBeleifsImportant','LQRHMSPrepHistUnderstandNews']]
        similarityMatrix = cosine_similarity(df)
        
        value = similarityMatrix[0][1]
        value = round(value,2)
        
        return 1 - value
        
        
        
        
        
        
        