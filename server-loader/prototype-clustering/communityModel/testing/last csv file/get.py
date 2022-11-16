import csv
import os
import sys

from context import dao

#from dao.dao_db_users_postapi import DAO_db_users_postapi
from dao.dao_api import DAO_api
from dao.dao_db_communities import DAO_db_community
import pandas as pd

def main():
    
    # Perform a get request
    daoAPI = DAO_api()
    #response = daoAPI.communityDescription("621e53cf0aa6aa7517c2afdd")
    response = daoAPI.communityList()
    print(response)
    
    
main()