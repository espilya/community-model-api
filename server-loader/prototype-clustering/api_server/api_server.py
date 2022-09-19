"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
import pymongo
from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

from context import dao
from dao.dao_db_perspectives import DAO_db_perspectives
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_flags import DAO_db_flags
from dao.dao_json import DAO_json
#from dao.deleteAndLoadDefaultData import deleteAndLoad
import time

from communityModel.hecht import CommunityModel

API_PORT = 8090

class Handler(BaseHTTPRequestHandler):

    # TODO:
    # - incorrect path or filename
    # - create thread for each connection/request
    # - refactor code

    def do_GET(self):
        """
        _get handler_
        API doc:
        - GET:
        http://localhost:8090/file/all                                      -> return all files -- List
        http://localhost:8090/file/{fileId}                                 -> return the first file with name equal to "fileId" -- JSON
        http://localhost:8090/perspectives/all                              -> ... -- List
        http://localhost:8090/perspectives/{perspectiveId}                  -> ... -- JSON
        http://localhost:8090/perspectives/{perspectiveId}/communities      -> Communities with the same "perspectiveId" -- List
        http://localhost:8090/index                                         -> return json files index (returns only files id) -- list
        - POST:
        Used only for redirection of POST requests from API Spice and access DB from here
        """
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        try:
            request = self.path.split("/")
            print("Request GET: ", request)
            first_arg = request[1]
            if first_arg == "file":
                self.__getFile(request[2])
            elif first_arg == "perspectives":
                self.__getPerspertives(request)
            elif first_arg == "index":
                self.__getIndex()
            else:
                print("-Error-")
                self.__set_response(404)
                self.wfile.write(
                    "-Error-\nThis GET request is not defined.\nGET request for {}".format(self.path).encode('utf-8'))
        except Exception as e:
            print("-Error-")
            print(e)
            if str(e) != "pymongo.errors.ServerSelectionTimeoutError":
                self.__set_response(500)
                self.wfile.write("-Error-\nGET request for {}".format(self.path).encode('utf-8'))
                # raise
            else:
                self.__set_response(500)
                self.wfile.write(
                    "-MongoDB connection timeout error-\nGET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        """
        _post handler_

        """
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        ok = False
        request = self.path.split("/")
        print("Request POST: ", request)
        first_arg = request[1]
        if first_arg == "perspective":
            perspective = loads(post_data.decode('utf-8'))
            daoPerspective = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
            ok = daoPerspective.insertPerspective(perspective)
            # <Update Community Model>
            # TODO: Hacer Llamada al Community Model
            # Esta hecho, solo que falta juntarlo
            # </Update Community Model>
        elif first_arg == "updateUsers":
            users = loads(post_data.decode('utf-8'))
            daoUsers = DAO_db_users("localhost", 27018, "spice", "spicepassword")
            ok = daoUsers.insertUser_API(users)
            
            # Activate flags associated to user/perspective pair (perspective makes use of one of the user's attributes (pname))
            daoPerspectives = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
            daoFlags = DAO_db_flags("localhost", 27018, "spice", "spicepassword")
            
            perspectives = daoPerspectives.getPerspectives()
            
            for user in users:
                for perspective in perspectives:
                    for similarityFunction in perspective['similarity_functions']:
                        if (similarityFunction['sim_function']['on_attribute']['att_name'] == user['pname']):
                            flag = {'perspective': perspective['id'], 'userid': user['userid'], 'flag': True}
                            daoFlags.updateFlag(flag)

        elif first_arg == "update_CM":
            # data = loads(post_data.decode('utf-8'))
            print("update_CM")
            # <Update Community Model>
            # TODO: Hacer Llamada al Community Model
            # Esta hecho, solo que falta juntarlo
            # </Update Community Model>
            
            # UPDATE CM 
            
            # Check if there is an update flag
            daoPerspectives = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
            daoFlags = DAO_db_flags("localhost", 27018, "spice", "spicepassword")

            flags = daoFlags.getFlags()
            for flag in flags:
                print(flag)
                perspective = daoPerspectives.getPerspective(flag["perspectiveId"])
                print("community model start")

                print("data from post requets: ", post_data)
                # Call to the community model
                communityModel = CommunityModel(perspective)
                communityModel.start()
                
                print("community model end")
                
                # Remove flag
                daoFlags.deleteFlag(flag)
            
            # END UPDATE CM
            ok = True
                
            
        if ok:
            self.__set_response(204)
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        else:
            self.__set_response(500)
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def __set_response(self, code, dataType='text/html'):
        self.send_response(code)
        self.send_header('Content-type', dataType)
        self.end_headers()

    def __getIndex(self):
        dao = DAO_db_community("localhost", 27018, "spice", "spicepassword")
        data = dao.getFileIndex()
        print(data)
        self.__set_response(200, 'application/json')
        self.wfile.write(dumps(data).encode(encoding='utf_8'))

    def __getPerspertives(self, request):
        dao = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
        perspectiveId = request[2]
        if perspectiveId == "all":
            data = dao.getPerspectives()
            self.__set_response(200, 'application/json')
            self.wfile.write(dumps(data).encode(encoding='utf_8'))
        else:
            if len(request) == 4 and request[3] == "communities":
                # perspectives/{perspectiveId}/communities
                result = []
                coms = DAO_db_community("localhost", 27018, "spice", "spicepassword").getCommunities()
                for com in coms:
                    if com["perspectiveId"] == perspectiveId:
                        result.append(com)
                self.__set_response(200, 'application/json')
                self.wfile.write(dumps(result).encode(encoding='utf_8'))
            else:
                data = dao.getPerspective(perspectiveId)
                print(data)
                if data:
                    self.__set_response(200, 'application/json')
                    self.wfile.write(dumps(data).encode(encoding='utf_8'))
                else:
                    self.__set_response(404)
                    self.wfile.write("File not found\nGET request for {}".format(self.path).encode('utf-8'))

    def __getFile(self, fileId):
        dao = DAO_db_community("localhost", 27018, "spice", "spicepassword")
        if fileId == "all":
            data = dao.getFileLists()
            self.__set_response(200, 'application/json')
            self.wfile.write(dumps(data).encode(encoding='utf_8'))
        else:
            data = dao.getFileList(fileId)
            if data:
                self.__set_response(200, 'application/json')
                self.wfile.write(dumps(data).encode(encoding='utf_8'))
            else:
                self.__set_response(404)
                self.wfile.write("File not found\nGET request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Handler, port=API_PORT):
    logging.basicConfig(level=logging.INFO)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


def importData():
    json5 = DAO_json("data/5.json")
    json5 = json5.getData()
    json6 = DAO_json("data/6.json").getData()
    jsonAll = DAO_json("data/Allperspectives.json").getData()

    daoC = DAO_db_community("localhost", 27018, "spice", "spicepassword")
    daoC.insertFileList("5", json5)
    daoC.insertFileList("6", json6)
    daoP = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
    daoP.insertPerspective(jsonAll)

if __name__ == '__main__':
    from sys import argv

    #deleteAndLoad()
    #importData()
    import socket   
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)   
    print("Your Computer Name is: "+hostname)   
    print("Your Computer IP Address is: "+IPAddr) 

    from ping3 import ping, verbose_ping
    print(ping('172.20.0.2:8080'))  # Returns delay in seconds.
    print(ping('172.20.0.3'))

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
