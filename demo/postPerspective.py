from context import dao
# First one is for local, second one for remote.
from dao.dao_api import DAO_api


import json

def main():

    #--------------------------------------------------------------------------------------------------------------------------
    #    Change server
    #--------------------------------------------------------------------------------------------------------------------------
    
    server = "http://localhost:8080"
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Change data file
    #--------------------------------------------------------------------------------------------------------------------------
    
    museum = 'HECHT'
    filename = 'hecht3.json'

    #--------------------------------------------------------------------------------------------------------------------------
    #    Read HECHT user data: all users except the last one
    #--------------------------------------------------------------------------------------------------------------------------

    route = "perspectives/" + museum + "/" + filename
    file = open(route)
    perspective = json.load(file)

    daoAPI = DAO_api()
    
    print("add perspective")
    response = daoAPI.addPerspective(perspective)
    print(response)
    print(response.text)
    

main()
