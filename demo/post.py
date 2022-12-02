from context import dao
# First one is for local, second one for remote.
from dao.dao_api import DAO_api
from dao.dao_api_remote import DAO_api_remote

import requests

import json

#--------------------------------------------------------------------------------------------------------------------------
#    Used to post demographic data (dict userid)
#--------------------------------------------------------------------------------------------------------------------------

def main():
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Change server
    #--------------------------------------------------------------------------------------------------------------------------
    
    server = "http://localhost:8080"
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Change data file
    #--------------------------------------------------------------------------------------------------------------------------
    
    museum = 'HECHT'
    filename = 'linked data hub.json'
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Read data
    #--------------------------------------------------------------------------------------------------------------------------
    
    fileRoute = 'data/' + museum + '/' + filename
    with open(fileRoute, 'r', encoding='utf8') as f:
        data = json.load(f) 

    #--------------------------------------------------------------------------------------------------------------------------
    #    Perform POST requests (interactions)
    #--------------------------------------------------------------------------------------------------------------------------
    
    postDict = data

    postDictKeys = ["English translation", "plutchik_emotions"]
    postDictKeys = postDict.keys()
    for userid in postDictKeys:
        userArray = postDict[userid]
        
        # print("key: " + str(userid))
        # print("value: " + str(userData))
        
        print("userid: " + str(userid))
        print("value: " + str(userArray))
        print("\n")
        response=requests.post(f'{server}/v1.1/users/{userid}/update-generated-content', json = userArray)
        print(response)
        print("\n\n")
            


main()