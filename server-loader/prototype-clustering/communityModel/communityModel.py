
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

class CommunityModel():

    def __init__(self,perspective,flag):
        """
        Construct of Community Model objects.

        Parameters
        ----------
            perspective: perspective object. Composed by:
                id, name
                algorithm: name and parameters
                similarity_functions: name, attribute, weight
            flag: flag object. Composed by:
                perspectiveId
                userid: user to update
        """
        self.perspective = perspective
        self.flag = flag
        self.percentageExplainability = 0.5
        
    def start(self):
        print("flag: " + str(self.flag))
        
        # Perspective was not found
        if (len(self.perspective) <= 0):
            return
        
        """
        if (self.flag['userid'] == ""):
            print("not doing the one that is added by default")
            return
        """   
            
        self.similarityMeasure = self.initializeComplexSimilarityMeasure()
        self.distanceMatrix = self.computeDistanceMatrix()
        self.clustering()
        # Compute the similarity between the new communities generated with self.perspective and all the other communities
        self.updateCommunitiesSimilarityCollection()
    
    def initializeComplexSimilarityMeasure(self):
        """
        Initializes the complex similarity measure associated to the given perspective

        Parameters
        ----------
        
        Returns
        -------
            similarityMeasure: ComplexSimilarityDAO
        """
        print("initialize complex similarity")
        print(self.perspective)
        print(self.perspective['similarity_functions'])
        daoCommunityModel = DAO_db_users()
        similarityDict = self.perspective['similarity_functions']
        similarityMeasure = ComplexSimilarityDAO(daoCommunityModel,similarityDict)
        return similarityMeasure
    
    def computeDistanceMatrix(self):
        """
        Method to calculate the distance matrix between all elements included in data.

        Parameters
        ----------
        
        Returns
        -------
            distanceMatrix: np.ndarray
        """

        # Load previous distance matrix
        daoDistanceMatrixes = DAO_db_distanceMatrixes()
        distanceMatrixJSON = daoDistanceMatrixes.getDistanceMatrix(self.perspective['id'])
        if (len(distanceMatrixJSON) == 0):
            distanceMatrix = np.empty([0,0])
        else:
            distanceMatrix = np.asarray(distanceMatrixJSON['distanceMatrix'])
        
        # Update distance matrix for all users (recalculate distance matrix)
        if (self.flag['userid'] == "flagAllUsers"):
            distanceMatrix = self.similarityMeasure.matrix_distance()
        # Update distance matrix for a user
        else:
            distanceMatrix = self.similarityMeasure.updateDistanceMatrix([self.flag['userid']], distanceMatrix)

        # Drop irrelevant parameters to explain communities
        #self.similarityMeasure.data.drop(['origin','source_id', '_id'], axis=1, inplace=True)
        self.similarityMeasure.data.drop(['origin','source_id'], axis=1, inplace=True)
        self.similarityMeasure.data = self.similarityMeasure.data.rename(columns={"userid":"user"})
        
        #return self.similarityMeasure.distanceMatrix
        return distanceMatrix
        
            
    def clusteringOLD(self):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            
        """
        percentageDefault = 0.78
        percentageDefault = 0.5
        
        algorithmName = self.perspective['algorithm']['name'] + "CommunityDetection"
        algorithmFile = "community_module.community_detection." + algorithmName 
        algorithmModule = importlib.import_module(algorithmFile)
        algorithmClass = getattr(algorithmModule,algorithmName[0].upper() + algorithmName[1:])
        
        community_detection_df = self.similarityMeasure.data.set_index('user')

        distanceMatrix = self.self.similarityMeasure.distanceMatrix
        community_detection = ExplainedCommunitiesDetection(algorithmClass, community_detection_df, distanceMatrix, self.perspective)

        n_communities, users_communities, self.medoids_communities = community_detection.search_all_communities(percentage=percentageDefault) 


        hecht_beliefR_pivot_df2 = community_detection_df.copy()
        hecht_beliefR_pivot_df2['community'] = users_communities.values()
        hecht_beliefR_pivot_df2.reset_index(inplace=True)
        hecht_beliefR_pivot_df2
        
        # Export to json
        self.exportCommunityClusteringJSON(hecht_beliefR_pivot_df2,community_detection,n_communities,percentageDefault,distanceMatrix)
    

    def clusteringExportFileRoute(self, percentageExplainability):
        abspath = os.path.dirname(__file__)
        #relpath = "clustering/" + self.perspective['name'] + " " + "(" + self.perspective['algorithm']['name'] + ")" 
        #relpath = "clustering/" + '(GAMGame_stories_RN_UNITO) ' + self.perspective['name'] + " "
        # relpath = "clustering/" + '(GAM RN) ' + self.perspective['name'] + " "
        relpath = "clustering/" 
        #relpath += "clusters generated/" + self.perspective["algorithm"]["name"] + "/"
        # relpath += "clusters Mine/" + self.perspective["algorithm"]["name"] + "/"

        relpath += self.perspective['name'] + " "
        relpath += " (" + str(percentageExplainability) + ")"
        relpath += ".json"
        route = os.path.normpath(os.path.join(abspath, relpath))
        
        return route
        
    def clustering(self, exportFile = "clustering.json"):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            percentageExplainability: minimum percentage of the most frequent value among 1+ main similarity features.
            
        """
        percentageExplainability = self.percentageExplainability
        
        # Initialize data
        algorithm = self.initializeAlgorithm()
        data = self.similarityMeasure.data
        data = data.set_index('user')
        
        #interactionObjectData = self.similarityMeasure.getInteractionObjectData()
        interactionObjectData = pd.DataFrame()
        
        # Get results
        community_detection = ExplainedCommunitiesDetection(algorithm, data, self.distanceMatrix, self.perspective)
        communityDict = community_detection.search_all_communities(percentage=percentageExplainability) 
        communityDict['perspective'] = self.perspective
        
        # Export to json
        data.reset_index(inplace=True)
        exportFile = self.clusteringExportFileRoute(percentageExplainability)
        jsonGenerator = CommunityJsonGenerator(interactionObjectData, data, self.distanceMatrix, communityDict, community_detection, self.perspective)
        jsonCommunity = jsonGenerator.generateJSON(exportFile)       
        
        # Save data to database
        insertedId = self.saveDatabase(jsonCommunity)
        
        return insertedId
    
    def initializeAlgorithm(self):
        algorithmName = self.perspective['algorithm']['name'] + "CommunityDetection"
        algorithmFile = "community_module.community_detection." + algorithmName 
        algorithmModule = importlib.import_module(algorithmFile)
        algorithmClass = getattr(algorithmModule,algorithmName[0].upper() + algorithmName[1:])
        
        return algorithmClass    
        

#--------------------------------------------------------------------------------------------------------------------------
#    Community jsons (visualization)
#--------------------------------------------------------------------------------------------------------------------------

    def saveDatabase(self,jsonCommunity):
        """
        daoCommunityModelVisualization = DAO_visualization()
        daoCommunityModelVisualization.drop()
        daoCommunityModelVisualization.insertJSON(jsonCommunity)
        """
        
        # Store distance matrix data
        # https://pynative.com/python-serialize-numpy-ndarray-into-json/
        daoDistanceMatrixes = DAO_db_distanceMatrixes()
        #daoDistanceMatrixes.drop()
        daoDistanceMatrixes.updateDistanceMatrix({'perspectiveId': self.perspective['id'], 'distanceMatrix': self.similarityMeasure.distanceMatrix.tolist()})
        
        # Store community data
        daoCommunityModelCommunity = DAO_db_community()
        # drop previous data
        daoCommunityModelCommunity.drop({'perspectiveId': self.perspective['id']})
        daoCommunityModelCommunity.dropFullList({'perspectiveId': self.perspective['id']})
        #daoCommunityModelCommunity.dropFullList()
        # add new data
        daoCommunityModelCommunity.insertFileList("", jsonCommunity)
        
#--------------------------------------------------------------------------------------------------------------------------
#   Compute similarity between communities
#--------------------------------------------------------------------------------------------------------------------------
    
    def updateCommunitiesSimilarityCollection(self):
        daoSimilarities = DAO_db_similarity()
        daoCommunities = DAO_db_community()
        
        # Get all the communities associated to the new perspective (A)
        communitiesA = daoCommunities.getCommunitiesPerspective(self.perspective["id"])
        
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
        print(self.similarityMeasure.data)
        print("\n\n")
        print(self.similarityMeasure.data.index)
        print("\n\n")
        
        userList = self.similarityMeasure.data['user'].to_list()
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
        
        
        
               
        
        
        
        

        
    
    
    