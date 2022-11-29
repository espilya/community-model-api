
from copy import copy, deepcopy
import requests
import pandas as pd

def     userToPostAPIFormat(userJSON):
        """
        Splits user json object into their attribute components
        according to the user model format

        Parameters
        ----------
        userJSON : json object encoding a citizen.

        """
        template = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx"
        }
        user = copy(userJSON)
        userTemplate = copy(template)
        # anadimos los campos necesarios
        # si es un id (viene del ugc) entonces lo guardamos con otro nombre
        # si es un _id (viene de mongodb) entonces lo ignoramos
        for key in user.keys():
            if key in template.keys():
                if key == "id":
                    userTemplate["ugc_id"] = user[key]
                elif key != "_id":
                    userTemplate[key] = user[key]

        items = (user.keys() - template.keys())
        usersAPI = []
        for item in items:
            userWithP = copy(userTemplate)
            userWithP["pname"] = item
            userWithP["pvalue"] = user[item]
            usersAPI.append(userWithP)

        return usersAPI

def main():
    # --------------------------------------------------------------------------------------------------------------------------
    #    Read HECHT user data: all users except the last one
    # --------------------------------------------------------------------------------------------------------------------------

    route = "data/hecht users.csv"
    # route = "data/hecht users one user.csv"
    # route = "data/HECHT 20221018.csv"
    # route = "data/hecht users 50.csv"
    df = pd.read_csv(route)

    # --------------------------------------------------------------------------------------------------------------------------
    #    fill NaN values
    # --------------------------------------------------------------------------------------------------------------------------

    # Fill NaN values with default ones (center value or dont know if exists)
    df['beliefR'].fillna('DK', inplace=True)
    df['beliefJ'].fillna('CantJudge', inplace=True)
    df['beliefE'].fillna('NoOpinion', inplace=True)
    df['DemographicsPolitics'].fillna('DK', inplace=True)
    df['DemographicsReligous'].fillna('R', inplace=True)

    # --------------------------------------------------------------------------------------------------------------------------
    #    perform post requests with user information
    # --------------------------------------------------------------------------------------------------------------------------

    users = []
    for ind in df.index:
        # print(df[' '][ind], df['beleifR'][ind], df['DemographicPolitics'][ind], df['DemographicReligous'][ind])
        user = {}
        user["userid"] = df['userid'][ind]
        user['_id'] = user["userid"]
        user["origin"] = ""
        user["source_id"] = ""
        user["ParticipantType"] = str(df["ParticipantType"][ind])  # Participant type
        user["beliefR"] = df['beliefR'][ind]  # beleifR
        user["beliefJ"] = df['beliefJ'][ind]  # beliefJ
        user["beliefE"] = df['beliefE'][ind]  # beliefE
        user["DemographicsPolitics"] = df['DemographicsPolitics'][ind]  # DemographicPolitics
        user["DemographicsReligous"] = df['DemographicsReligous'][ind]  # DemographicReligous

        # Split user information into user model dict
        usersAPI = userToPostAPIFormat(user)
        # print(usersAPI)
        # usersAPI = [usersAPI[0]]

        for user in usersAPI:
            postUserData = [user]
            response = requests.post("http://localhost:8080/v1.1/users/{}/update-generated-content".format(user['userid']),
                                     json=postUserData)
            print("post api " + str(postUserData))
            print(response)
            print(response.text)
            print("\n\n")


main()
