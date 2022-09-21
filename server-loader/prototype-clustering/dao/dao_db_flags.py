from bson.json_util import dumps, loads


from context import dao
from dao.dao_class import DAO

from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_flags(DAO):
    """
    DAO for accessing flag related data in MongoDB
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
        # print("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))
        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(MONGO_USER, MONGO_PASS,
                                                                                           MONGO_HOST, MONGO_PORT)
        self.mongo = MongoClient(uri)
        # self.mongo = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password)) #MongoClient("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))

        self.db_flags = self.mongo.spiceComMod.flags


    def getData(self):
        pass
    

    def getFlag(self):
        """
        :Return:
            List with all flags, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_flags.find({})
        dataList = loads(dumps(list(dataList)))
        return dataList[0]

    def deleteFlag(self, flagJSON):
        """
        :Parameters:
            flagJSON: Flag/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        self.db_flags.delete_one(flagJSON)
        

    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_flags.delete_many({})

    def insertFlag(self, flagJSON):
        """
        :Parameters:
            flagJSON: flag associated to the perspective and the user.
        """
        temp = copy(flagJSON)
        if type(temp) is list:
            self.db_flags.insert_many(temp)
        else:
            self.db_flags.insert_one(temp)
            
    def updateFlag(self, flagJSON):
        key = {'perspective': flagJSON['perspective'], 'userId': flagJSON['userId']}
        self.db_flags.update_one(key,{"$set": flagJSON},upsert=True)
 
    def getFlags(self):
        """
        :Return:
            flags, Type: List[<class 'dict'>]
        """
        data = self.db_flags.find({}, {"_id": 0})
        return loads(dumps(list(data)))
        
    def deleteFlag(self, flagId):
        """
        :Parameters:
            flagId: Type: <class 'str'>
        """
        self.db_flags.delete_one({'id': flagId})
        
        
