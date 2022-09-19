

#--------------------------------------------------------------------------------------------------------------------------
#    Import
#--------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np

import ipywidgets as widgets
from ipywidgets import AppLayout
import IPython.display as pyDis


from context import community_module

#from communityModel.debug import Debugger

# In[96]:





# In[157]:


# similarity measures
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO
from community_module.similarity.hechtBeliefRSimilarityDAO import HechtBeliefRSimilarityDAO
from community_module.similarity.hechtBeliefJSimilarityDAO import HechtBeliefJSimilarityDAO
from community_module.similarity.hechtDemographicReligiousSimilarityDAO import HechtDemographicReligiousSimilarityDAO
from community_module.similarity.hechtDemographicPoliticsSimilarityDAO import HechtDemographicPoliticsSimilarityDAO


# In[175]:


from dao.dao_csv import DAO_csv
from dao.dao_db_users import DAO_db_users
#import dao.import_data_api



from community_module.community_detection.agglomerativeCommunityDetectionDistanceMatrix import AgglomerativeCommunityDetectionDistanceMatrix
from community_module.community_detection.explainedCommunitiesDetectionDistanceMatrix import ExplainedCommunitiesDetectionDistanceMatrix

# json
from community_module.community_detection.communityJsonGenerator import CommunityJsonGenerator

# dao community & visualization
from dao.dao_db_communities import DAO_db_community
#from dao.dao_visualization import DAO_visualization


import importlib


#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class CommunityModel():

    """
        Arguments:
            perspective: 
    """
    def __init__(self,perspective):
        self.perspective = perspective
        
    
    """

    """
    def start(self):
        self.computeDistanceMatrix()
        self.clustering(self.similarityMeasure)
    
    """

    """
    def computeDistanceMatrix(self):
        daoHecht = DAO_db_users("localhost", 27018, "spice", "spicepassword")
        #similarityDict = self.perspective.similarity_functions
        
        similarityDict = {}
        for similarityFunction in self.perspective['similarity_functions']:
            similarityName = similarityFunction['sim_function']['name']
            similarityFile = "community_module.similarity." + similarityName[0].lower() + similarityName[1:]
            similarityModule = importlib.import_module(similarityFile)
            print(similarityName)
            print(similarityFile)
            similarityClass = getattr(similarityModule,similarityName)
            print(similarityClass)
            
            similarityDict[similarityClass] = similarityFunction['sim_function']['weight']
        
        print(similarityDict)
        
        similarityDict = {
            HechtBeliefRSimilarityDAO: 0.8,
            HechtBeliefJSimilarityDAO: 0.6,
            HechtDemographicReligiousSimilarityDAO: 0.2,
            HechtDemographicPoliticsSimilarityDAO: 0.2   
        }
        
        print(similarityDict)
        
        similarityMeasure = ComplexSimilarityDAO(daoHecht,similarityDict)
        print(similarityMeasure.data)
        self.distanceMatrix = similarityMeasure.matrix_distance()
        
        similarityMeasure.data.drop(['origin','source_id', '_id', 'ugc_id'], axis=1, inplace=True)
        similarityMeasure.data = similarityMeasure.data.rename(columns={"userid":"user"})
        self.similarityMeasure = similarityMeasure
    
    """
    
    """
    def clustering(self,similarityMeasure):
        percentageDefault = 0.78
        percentageDefault = 0.5
        
        community_detection_df = similarityMeasure.data.set_index('user')
        distanceMatrix = self.similarityMeasure.distanceMatrix
        community_detection = ExplainedCommunitiesDetectionDistanceMatrix(AgglomerativeCommunityDetectionDistanceMatrix, community_detection_df, distanceMatrix)

        n_communities, users_communities = community_detection.search_all_communities(percentage=percentageDefault)

        hecht_beliefR_pivot_df2 = community_detection_df.copy()
        hecht_beliefR_pivot_df2['community'] = users_communities.values()
        hecht_beliefR_pivot_df2.reset_index(inplace=True)
        hecht_beliefR_pivot_df2
        
        # Explicamos comunidades
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


        jsonGenerator = CommunityJsonGenerator(json_df,community_detection,n_communities,percentageDefault,distanceMatrix)
        #jsonCommunity = jsonGenerator.generateJSON("../jsonVisualization/HECHT.json")
        
        jsonCommunity = jsonGenerator.generateJSON("../examples/jsonVisualization/HECHT.json")
        
        
        # Community jsons (visualization)
        self.saveDatabase(jsonCommunity)
    

#--------------------------------------------------------------------------------------------------------------------------
#    Community jsons (visualization)
#--------------------------------------------------------------------------------------------------------------------------

    def saveDatabase(self,jsonCommunity):
        """
        daoHechtVisualization = DAO_visualization()
        daoHechtVisualization.drop()
        daoHechtVisualization.insertJSON(jsonCommunity)
        """
        
        daoHechtCommunity = DAO_db_community("localhost", 27018, "spice", "spicepassword")
        daoHechtCommunity.drop()
        daoHechtCommunity.insertFileList("", jsonCommunity)
    
    
    
    
               
        
        
        
        

        
    
    
    