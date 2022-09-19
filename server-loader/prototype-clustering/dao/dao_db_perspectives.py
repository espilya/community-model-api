import json
from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from context import dao
from dao.dao_class import DAO


# {
#     _id: "0",
#     perspectiveId: "0",
#     description: "Opinions regarding Roman Rebellion",
#     similarities: {
#         "belief Roman Rebellion": 0.7
#         "openess": 0.2
#         "history" : 0.1
#     }
# }
# Similarities: key (attribute); value (weight or importance)

class DAO_db_perspectives(DAO):
    """
    DAO for accessing perspective related data in MongoDB
    Contains basics CRUD operaions
    """

    def __init__(self, MONGO_HOST="localhost", MONGO_PORT=27018, MONGO_USER="", MONGO_PASS="", MONGO_DB="spiceComMod"):
        """
        :Parameters:
            MONGO_HOST: mongodb address, Default value: "localhost"
            MONGO_PORT: mongodb port, Default value: 27018
            MONGO_USER: mongodb user, Default value: ""
            MONGO_PASS: mongodb pass, Default value: ""
            MONGO_DB: mongodb db name, Default value: "spiceComMod"
        """
        super().__init__(MONGO_HOST)

        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(MONGO_USER, MONGO_PASS,
                                                                                           MONGO_HOST, MONGO_PORT)
        self.mongo = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db_perspectives = self.mongo.spiceComMod.perspectives

    def getData(self):
        return self.getPerspectives()

    def insertPerspective(self, perspectiveJSON):
        """
        :Parameters:
            perspectiveJSON: Perspective, Type: <class 'dict'>
        """
        temp = copy(perspectiveJSON)
        if type(temp) is list:
            self.db_perspectives.insert_many(temp)
        else:
            self.db_perspectives.insert_one(temp)

    def getPerspectives(self):
        """
        :Return:
            perspectives, Type: List[<class 'dict'>]
        """
        data = self.db_perspectives.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getPerspective(self, perspectiveId):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
        :Return:
            perspective, Type: <class 'dict'>
        """
        data = {}
        data = self.db_perspectives.find({"id": perspectiveId}, {"_id": 0})

        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]

    def updatePerspective(self, perspectiveId, newJSON):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
            newJSON: JSON value, Type: <class 'dict'>
        """
        temp = copy(newJSON)
        response = self.db_perspectives.replace_one({"id": perspectiveId}, temp)

    def deletePerspective(self, perspectiveId):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
        """
        self.db_perspectives.delete_one({'id': perspectiveId})

    def drop(self):
        """
            MongoDB Delete Documents in this collection
        """
        self.db_perspectives.delete_many({})
