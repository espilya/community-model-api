import os
from context import dao
from dao.dao_class import DAO
from pymongo import MongoClient
from bson.json_util import dumps, loads


class DAO_db(DAO):
    """
    Superclass for all dao's db
    """

    def __init__(self):
        self.db_host = os.environ['DB_HOST']
        self.db_user = os.environ['DB_USER']
        self.db_password = os.environ['DB_PASSWORD']
        self.db_name = os.environ['DB_NAME']
        self.db_port = os.environ['DB_PORT']

        # print("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))
        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(self.db_user, self.db_password,
                                                                                           self.db_host, self.db_port)
        self.mongo = MongoClient(uri)
        # self.mongo = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # self.mongo = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password)) #MongoClient("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))

        super().__init__(self.db_host)

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

    def dumpDB(self):
        client = self.mongo
        database = client[self.db_name]
        collections = database.list_collection_names()
        print("Collections: ", collections)

        dump = {}
        for i, collection_name in enumerate(collections):
            col = getattr(database, collections[i])
            collection = col.find()
            collection = loads(dumps(list(collection)))
            dump[collections[i]] = collection
        # print(dump)

        return dump



