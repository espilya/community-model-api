import csv
import os
import sys

from context import dao
from dao.dao_db_users_testing import DAO_db_users
from dao.dao_api import DAO_api
import pandas as pd

import json

def main():

    #--------------------------------------------------------------------------------------------------------------------------
    #    Read HECHT user data: all users except the last one
    #--------------------------------------------------------------------------------------------------------------------------
    
    route = 'data/Hecht_DEGARI_emotions SPICEUMProperty.json'
    df = pd.read_json(route)
    
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Fill NaN values
    #--------------------------------------------------------------------------------------------------------------------------
    
    df.fillna('unknown',inplace=True)
    
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Export to json
    #--------------------------------------------------------------------------------------------------------------------------
    
    result2 = df.to_json(orient='records')
    parsed = json.loads(result2)
    filename = 'data/Hecht_DEGARI_emotions SPICEUMProperty 2.json'
    with open(filename, "w") as outfile:
        #json.dump(user_interactions.to_dict('records'), outfile, indent=4)
        json.dump(parsed, outfile, indent=4)
    
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Read HECHT user data: all users except the last one
    #--------------------------------------------------------------------------------------------------------------------------
    
    filename = 'data/Hecht_DEGARI_emotions SPICEUMProperty 2.json'
    with open(filename, 'r', encoding='utf8') as f:
        data = json.load(f)
        
    #print(data)
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Perform POST requests
    #--------------------------------------------------------------------------------------------------------------------------
    
    daoAPI = DAO_api()
    
    #data = [data[0]]
    
    for userModelData in data:
        
        # For some reason it doesnt work without adding these three keys
        userModelData['id'] = 'xxx'
        userModelData['origin'] = ''
        userModelData['source_id'] = ''
        
        
        
        
        postUserData = [userModelData]
        response = daoAPI.updateUser(userModelData['userid'],postUserData) 

        print("post api " + str(postUserData))
        print(response)
        print("\n\n")


main()










"""


    #--------------------------------------------------------------------------------------------------------------------------
    #    perform post requests with user information
    #--------------------------------------------------------------------------------------------------------------------------
    
    users = []
    for ind in df.index:
        # print(df[' '][ind], df['beleifR'][ind], df['DemographicPolitics'][ind], df['DemographicReligous'][ind])
        user = {}
        user["userid"] = df['userid'][ind]
        user['_id'] = user["userid"]
        user["origin"] = ""
        user["source_id"] = ""
        user["ParticipantType"] = str(df["ParticipantType"][ind]) # Participant type
        user["beliefR"] = df['beliefR'][ind]  # beleifR
        user["beliefJ"] = df['beliefJ'][ind]  # beliefJ
        user["beliefE"] = df['beliefE'][ind]  # beliefE
        user["DemographicsPolitics"] = df['DemographicsPolitics'][ind]  # DemographicPolitics
        user["DemographicsReligous"] = df['DemographicsReligous'][ind]  # DemographicReligous
        
        # Split user information into user model dict
        usersAPI = daoU.userToPostAPIFormat(user)

        for user in usersAPI:
            postUserData = [user]
            response = daoAPI.updateUser(user['userid'],postUserData)

    
main()

"""