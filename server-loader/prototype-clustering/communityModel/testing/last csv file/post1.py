import csv
import os
import sys

from context import dao
from dao.dao_db_users_testing import DAO_db_users
from dao.dao_api import DAO_api
import pandas as pd

def main():
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Read HECHT user data: all users except the last one
    #--------------------------------------------------------------------------------------------------------------------------
    
    route = "data/hecht users.csv"
    # route = "data/hecht users one user.csv"
    #route = "data/HECHT 20221018.csv"
    #route = "data/hecht users 50.csv"
    df = pd.read_csv(route)
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    fill NaN values
    #--------------------------------------------------------------------------------------------------------------------------
    
    # Fill NaN values with default ones (center value or dont know if exists)
    df['beliefR'].fillna('DK',inplace=True)
    df['beliefJ'].fillna('CantJudge',inplace=True)
    df['beliefE'].fillna('NoOpinion',inplace=True)
    df['DemographicsPolitics'].fillna('DK',inplace=True)
    df['DemographicsReligous'].fillna('R',inplace=True)
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    remove users from database
    #--------------------------------------------------------------------------------------------------------------------------
      
    daoU = DAO_db_users()
    #daoU.drop()
    
    daoAPI = DAO_api()

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
        #print(usersAPI)
        #usersAPI = [usersAPI[0]]

        for user in usersAPI:
            postUserData = [user]
            response = daoAPI.updateUser(user['userid'],postUserData)
            
            print("post api " + str(postUserData))
            print(response)
            print("\n\n")

    
main()
