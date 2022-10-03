import csv
import os
import sys

from context import dao

from dao.dao_db_users_postapi import DAO_db_users_postapi
from dao.dao_api import DAO_api
from dao.dao_db_communities import DAO_db_community
import pandas as pd

def main():

    communities = [{
        "id": "621e53cf0aa6aa7517c2afdd",
        "community-type": "explicit",
        "name": "elderly",
        "perspectiveId": "1000",
        "explanation": "People above 65",
        "users": [
            "23",
            "28"
        ],
    }, {
        "id": "721e53cf0aa6aa7517c2afdd",
        "community-type": "implicit",
        "explanation": "lorem ipsum",
        "perspectiveId": "1000",
        "name": "impl_1",
        "users": [
            "44",
            "23"
        ]
    }, {
        "id": "821e53cf0aa6aa7517c2afdd",
        "community-type": "explicit",
        "name": "teenager",
        "perspectiveId": "100",
        "explanation": "People whose age is between 12 and 17",
        "users": [
            "44",
            "56"
        ],
    }]
    
    daoC = DAO_db_community()
    daoC.drop()
    #daoC.dropFullList()
    #daoC.insertCommunity(communities)
    
    # Perform a get request
    daoAPI = DAO_api()
    #response = daoAPI.communityDescription("621e53cf0aa6aa7517c2afdd")
    response = daoAPI.perspectiveList()
    print(response)
    
    
main()