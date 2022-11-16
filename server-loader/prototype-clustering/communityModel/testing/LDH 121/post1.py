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
    
    """
    print(df.loc[df['userid'] == 'PH236328'])
    print("\n\n")
    """
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Fill NaN values
    #--------------------------------------------------------------------------------------------------------------------------
    
    df.fillna('',inplace=True)
    
    """
    print(df.loc[df['userid'] == 'PH236328'])
    print(df.loc[df['userid'] == 'PH236328'].columns)
    print(df.loc[df['userid'] == 'PH236328'][['beliefJ']])
    """
    
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Export to json
    #--------------------------------------------------------------------------------------------------------------------------
    
    result2 = df.to_json(orient='records')
    parsed = json.loads(result2)
    filename = 'data/Hecht_DEGARI_emotions SPICEUMProperty 2.json'
    with open(filename, "w") as outfile:
        #json.dump(user_interactions.to_dict('records'), outfile, indent=4)
        json.dump(parsed, outfile, indent=4)
    
    """
    #--------------------------------------------------------------------------------------------------------------------------
    #    fill NaN values
    #--------------------------------------------------------------------------------------------------------------------------
    
    # Fill NaN values with default ones (center value or dont know if exists)
    df['beliefR'].fillna('DK',inplace=True)
    df['beliefJ'].fillna('CantJudge',inplace=True)
    df['beliefE'].fillna('NoOpinion',inplace=True)
    df['DemographicsPolitics'].fillna('DK',inplace=True)
    df['DemographicsReligous'].fillna('R',inplace=True)
    """
    
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
        #userModelData = dict([(x, y) for x, y in userModelData.items() if not x.startswith('_timestamp')])
        #userModelData = dict([(x, y) for x, y in userModelData.items() if not x.startswith('_')])
        
        """
        userModelData.pop("_id", "")
        userModelData.pop("doctype", "")
        userModelData.pop("category", "")
        userModelData.pop("createAt", "")
        userModelData.pop("updatedAt", "")
        userModelData.pop("_timestamp", "")
        """
        
        # For some reason it doesnt work without adding these three keys
        userModelData['id'] = 'xxx'
        userModelData['origin'] = ''
        userModelData['source_id'] = ''
        
        
        
        print("userModel inserts " + str(userModelData))
        print("\n")
        print(userModelData['userid'])
        postUserData = [userModelData]
        response = daoAPI.updateUser(userModelData['userid'],postUserData) 
        print("\n")
        print(response)
        print("inserted successfully")
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