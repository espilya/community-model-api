from context import dao
from dao.dao_class import DAO
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity
from dao.dao_db_perspectives import DAO_db_perspectives
from dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from dao.dao_csv import DAO_csv
from dao.dao_json import DAO_json
from dao.dao_api import DAO_api
from dao.dao_linkedDataHub import DAO_linkedDataHub

from dao.dao_db_flags import DAO_db_flags

from communityModel.testing.dataLoader import DataLoader


import json

def clear():
    print("1")
    daoF = DAO_db_flags()
    print("1a")
    #flags = daoF.getFlags()
    #print(flags)
    daoF.drop()
    
    print("2")
    daoC = DAO_db_community()
    daoC.drop()
    daoC.dropFullList()
    
    print("3")
    daoU = DAO_db_users()
    daoU.drop()
    
    print("4")
    daoDistanceMatrixes = DAO_db_distanceMatrixes()
    daoDistanceMatrixes.drop()
    
    print("5")
    daoSimilarity = DAO_db_similarity()
    #daoSimilarities.drop()
    

def initialize():
    daoPerspectives = DAO_db_perspectives()
    daoPerspectives.drop()
    
    route = DataLoader().fileRoute("../perspectives/all.json")
    file = open(route)
    perspectives = json.load(file)
    print(perspectives)
    file.close()
    
    daoPerspectives.insertPerspective(perspectives)
    
def prepareDatabase():
    clear()
    initialize()
    

clear()
initialize()
