import os

#--------------------------------------------------------------------------------------------------------------------------
#    Import
#--------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from context import community_module

from communityModel.debug import Debugger
# json
from communityModel.communityJsonGenerator import CommunityJsonGenerator

# In[96]:





# In[157]:


# similarity measures
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO
from community_module.similarity.tableSimilarityDAO import TableSimilarityDAO

# In[175]:


from dao.dao_csv import DAO_csv
from dao.dao_db_users import DAO_db_users
#import dao.import_data_api

from dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes


from community_module.community_detection.agglomerativeCommunityDetectionDistanceMatrix import AgglomerativeCommunityDetectionDistanceMatrix
from community_module.community_detection.explainedCommunitiesDetectionDistanceMatrix import ExplainedCommunitiesDetectionDistanceMatrix



# dao community & visualization
from dao.dao_db_communities import DAO_db_community
#from dao.dao_visualization import DAO_visualization



import json


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
        
    def start(self):
        self.similarityMeasure = self.initializeComplexSimilarityMeasure()
        self.distanceMatrix = self.computeDistanceMatrix()
        self.clustering(self.similarityMeasure)
    
    def initializeComplexSimilarityMeasure(self):
        """
        Initializes the complex similarity measure associated to the given perspective

        Parameters
        ----------
        
        Returns
        -------
            similarityMeasure: ComplexSimilarityDAO
        """
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
        
        # Update distance matrix
        self.similarityMeasure.updateDistanceMatrix([self.flag['userid']], distanceMatrix)

        # Drop irrelevant parameters to explain communities
        self.similarityMeasure.data.drop(['origin','source_id', '_id'], axis=1, inplace=True)
        self.similarityMeasure.data = self.similarityMeasure.data.rename(columns={"userid":"user"})
        
        return self.similarityMeasure.distanceMatrix
        
            
    def clustering(self,similarityMeasure):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            
        """
        percentageDefault = 0.78
        percentageDefault = 0.5
        
        # For now required to get users in community information (JSON)
        community_detection_df = similarityMeasure.data.set_index('user')

        distanceMatrix = self.similarityMeasure.distanceMatrix
        community_detection = ExplainedCommunitiesDetectionDistanceMatrix(AgglomerativeCommunityDetectionDistanceMatrix, community_detection_df, distanceMatrix)

        n_communities, users_communities, self.medoids_communities = community_detection.search_all_communities(percentage=percentageDefault) 


        hecht_beliefR_pivot_df2 = community_detection_df.copy()
        hecht_beliefR_pivot_df2['community'] = users_communities.values()
        hecht_beliefR_pivot_df2.reset_index(inplace=True)
        hecht_beliefR_pivot_df2
        
        
        # Explicamos comunidades
        """
        users_without_community = []

        for c in range(n_communities):
                community_data = community_detection.get_community(c, percentage=percentageDefault)
                
                if len(community_data['members']) > 1:
                
                    print('---------------------')
                    print('COMMUNITY -', community_data['name'])
                    print('\t- N. Members:', len(community_data['members']))
                    print('\t- Properties:')

                    for k in community_data['properties'].keys():
                        print('\t\t-', k, community_data['properties'][k])
                else:
                    users_without_community.extend(community_data['members'])
                    
                    
        print('---------------------')
        print('N. USERS WITHOUT COMMUNITY -', len(users_without_community))
        """
        
        # Export to json
        self.exportCommunityClusteringJSON(hecht_beliefR_pivot_df2,community_detection,n_communities,percentageDefault,distanceMatrix)
        
#--------------------------------------------------------------------------------------------------------------------------
#    Complex similarity (HECHT) - Export JSON (with file)
#--------------------------------------------------------------------------------------------------------------------------

    def exportCommunityClusteringJSON(self, hecht_beliefR_pivot_df2,community_detection,n_communities,percentageDefault,distanceMatrix):
        # Group explicit community properties in one column
        json_df = hecht_beliefR_pivot_df2.copy()
        json_df['id'] = json_df['user']
        json_df['label'] = json_df['user']
        json_df = json_df.rename(columns={"community":"group"})
        columns = ['DemographicPolitics','DemographicReligous']
        columns = ['DemographicPolitics','DemographicReligous','beleifR','beliefJ']
        json_df['explicit_community'] = json_df[columns].to_dict(orient='records')
        json_df


        # In[205]:


        jsonGenerator = CommunityJsonGenerator(json_df,community_detection,n_communities,percentageDefault,distanceMatrix,self.perspective['id'], self.medoids_communities)
        #jsonCommunity = jsonGenerator.generateJSON("../jsonVisualization/HECHT.json")

        #jsonCommunity = jsonGenerator.generateJSON("/app/prototype-clustering/examples/jsonVisualization/clustering.json")
        #jsonCommunity = jsonGenerator.generateJSON("/app/prototype-clustering/communityModel/jsonVisualization/clustering.json")       
        
        jsonCommunity = jsonGenerator.generateJSON("clustering.json")       
        
        # Community jsons (visualization)
        self.saveDatabase(jsonCommunity)
    

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
        
        
    
    
    
    
               
        
        
        
        

        
    
    
    