
#--------------------------------------------------------------------------------------------------------------------------
#    Python libraries
#--------------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import importlib

from inspect import getsourcefile
from os.path import abspath
import sys

#--------------------------------------------------------------------------------------------------------------------------
#    Custom Class
#--------------------------------------------------------------------------------------------------------------------------

from context import community_module

# Community model tools
from communityModel.communityJsonGenerator import CommunityJsonGenerator

# Community detection
from community_module.community_detection.explainedCommunitiesDetection import ExplainedCommunitiesDetection

# similarity measures
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO

# dao
from dao.dao_csv import DAO_csv
from dao.dao_json import DAO_json
from dao.dao_db_users import DAO_db_users
from dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity


#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class CommunitiesSimilarityModel():

    def __init__(self,perspectiveId, data):
        """
        Construct of Community Model objects.

        Parameters
        ----------
            perspectiveId:
                id of the perspective to which the communities we want to calculate similarity on belong
        """
        self.perspectiveId = perspectiveId
        self.data = data
        self.updateCommunitiesSimilarityCollection()
        
    
#--------------------------------------------------------------------------------------------------------------------------
#   Compute similarity between communities
#--------------------------------------------------------------------------------------------------------------------------
    
    def updateCommunitiesSimilarityCollection(self):
        daoSimilarities = DAO_db_similarity()
        daoCommunities = DAO_db_community()
        
        # Get all the communities associated to the new perspective (A)
        #communitiesA = daoCommunities.getCommunitiesPerspective(self.perspective["id"])
        communitiesA = daoCommunities.getCommunitiesPerspective(self.perspectiveId)
        
        # Get all the communities (B)
        communitiesB = daoCommunities.getCommunities()
        
        # Get index of the medoid explanation
        indexMedoidExplanation = self.getIndexMedoidExplanation(communitiesB)
        
        print("index medoid explanation is : " + str(indexMedoidExplanation))

        # Compute similarity between the communities in A and the communities in B
        for communityA in communitiesA:
            for communityB in communitiesB:
                similarityCommunities = self.computeCommunitiesSimilarity(communityA, communityB, indexMedoidExplanation)
                # Insert it in the two different orders
                similarityJson = {
                    "similarity-function": "similarityMedoidCommunitiesDAO",
                    "value": similarityCommunities,
                }
                daoSimilarities.updateSimilarity(communityA['id'], communityB['id'], similarityJson)
                
                similarityJson = {
                    "similarity-function": "similarityMedoidCommunitiesDAO",
                    "value": similarityCommunities,
                }
                daoSimilarities.updateSimilarity(communityB['id'], communityA['id'], similarityJson)

    
    def getIndexMedoidExplanation(self, communitiesB):
        if (len(communitiesB) <= 0):
            return 0
        else:
            community = communitiesB[0]
            indexMedoidExplanation = 0
            index = 0
            found = False
            
            while found == False and index < len(community['explanations']):
                explanation = community['explanations'][index]
                if (explanation['explanation_type'] == 'medoid'):
                    found = True
                    indexMedoidExplanation = index
                index += 1
            
            return indexMedoidExplanation
    
    def computeCommunitiesSimilarity(self, communityA, communityB, indexMedoidExplanation):
        # Get distance matrixes between communities
        perspectiveA = communityA["perspectiveId"]
        perspectiveB = communityB["perspectiveId"]
        
        daoDistanceMatrixes = DAO_db_distanceMatrixes()
        
        distanceMatrixAJSON = daoDistanceMatrixes.getDistanceMatrix(perspectiveA)
        distanceMatrixA = np.asarray(distanceMatrixAJSON['distanceMatrix'])
        
        distanceMatrixBJSON = daoDistanceMatrixes.getDistanceMatrix(perspectiveB)
        distanceMatrixB = np.asarray(distanceMatrixBJSON['distanceMatrix'])
        
        
        
        # Get medoids (dm: distance matrix)
        medoidA = communityA['explanations'][indexMedoidExplanation]['explanation_data']['id']
        medoidB = communityB['explanations'][indexMedoidExplanation]['explanation_data']['id']
        
        print("data: \n\n\n")
        print(self.data)
        print("\n\n")
        print(self.data.index)
        print("\n\n")
        
        userList = self.data['user'].to_list()
        dmIndexA = userList.index(medoidA)
        dmIndexB = userList.index(medoidB)
        
        print("index 1: " + str(dmIndexA))
        print("index 2: " + str(dmIndexB))
        print("\n")
        
        # Get distance between medoids (by distanceMatrixA and distanceMatrixB)
        print("distance matrix A")
        print(distanceMatrixA)
        print("\n")
        print("distance matrix B")
        print(distanceMatrixB)
        print("\n")
        
        distanceA = distanceMatrixA[dmIndexA,dmIndexB]
        distanceB = distanceMatrixB[dmIndexA,dmIndexB]
        
        print("distanceA: " + str(distanceA))
        print("distanceB: " + str(distanceB))
        
        distanceCommunities = (distanceA + distanceB) / 2
        print("distanceCommunities: " + str(distanceCommunities))
        distanceCommunities = int(distanceCommunities * 100) / 100
        print("distanceCommunities: " + str(distanceCommunities))
        similarityCommunities = 1 - distanceCommunities
        
        print("similarity between communities: " + str(similarityCommunities))
        
        return similarityCommunities
        
        
        
               
        
        
        
        

        
    
    
    