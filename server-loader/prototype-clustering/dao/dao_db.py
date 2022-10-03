import os
from context import dao
from dao.dao_class import DAO
from pymongo import MongoClient

class DAO_db(DAO):
    """
    Superclass for all dao's db
    """
    def __init__(self):
        db_host = os.environ['DB_HOST']
        db_user = os.environ['DB_USER']
        db_password = os.environ['DB_PASSWORD']
        db_name = os.environ['DB_NAME']
        db_port = os.environ['DB_PORT']
        
        # print("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))
        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(db_user, db_password,
                                                                                           db_host, db_port)
        self.mongo = MongoClient(uri)
        # self.mongo = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # self.mongo = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password)) #MongoClient("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))

        super().__init__(db_host)
        
        """
        print("\n")
        print("dao db users ports")
        print(db_host)
        print(db_port)
        print(db_user)
        print(db_password)
        print(db_name)
        print("\n")
        """
        
        

        