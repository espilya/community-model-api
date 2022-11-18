# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

import importlib

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
        for similarityFunction in similarityDict:
            similarityName = similarityFunction['sim_function']['name']
            similarityFile = "community_module.similarity." + similarityName[0].lower() + similarityName[1:]
            similarityModule = importlib.import_module(similarityFile)
            similarityClass = getattr(similarityModule,similarityName)
            similarityMeasure = similarityClass(dao,similarityFunction['sim_function'])
            self.similarityDict[similarityMeasure] = similarityFunction['sim_function'].get('weight',0.5)
        
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
        for similarity, weight in self.similarityDict.items():
            simDistance = similarity.distance(elemA,elemB) 
            simDistance2 = simDistance * weight
            
            complexDistance += simDistance2
            complexWeight = complexWeight + weight 

        complexDistance = complexDistance / complexWeight
        
        return complexDistance
        

        