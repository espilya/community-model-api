from context import dao
from dao.dao_class import DAO
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity
from dao.dao_db_perspectives import DAO_db_perspectives
from dao.dao_csv import DAO_csv
from dao.dao_json import DAO_json
from dao.dao_api import DAO_api
from dao.dao_linkedDataHub import DAO_linkedDataHub

from dao.dao_db_flags import DAO_db_flags


import json

def clear():
    daoF = DAO_db_flags("localhost", 27018, "spice", "spicepassword")
    daoF.drop()
    
    daoC = DAO_db_community("localhost", 27018, "spice", "spicepassword")
    daoC.drop()
    daoC.dropFullList()

def initialize():
    daoPerspectives = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
    daoPerspectives.drop()
    
    file = open("../perspectives/all.json")
    perspectives = json.load(file)
    print(perspectives)
    file.close()
    
    daoPerspectives.insertPerspective(perspectives)
    

clear()
#initialize()
