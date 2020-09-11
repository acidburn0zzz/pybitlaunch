from .BaseAPI import BaseAPI, GET, POST, PUT, DELETE
from .SSHKeys import SSHKey

# Server object to store a new servers parameters
class Server(object):
    def __init__(self, name = None, hostID = None, hostImageID = None, sizeID = None, regionID = None, sshKeys = None, password = None, initscript = None):
        self.name = name
        self.hostID = hostID
        self.hostImageID = hostImageID
        self.sizeID = sizeID
        self.regionID = regionID
        self.sshKeys = sshKeys
        self.password = password
        self.initscript = initscript

# Server object service to handle object functions
class ServerService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(ServerService, self).__init__(*args, **kwargs)
    
    # List all servers on account
    def List(self):
        # Get data from API
        data = self.getData("servers")

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None

    # Send request to create a new server
    def Create(self, server):
        # If statement block to check for valid server object
        if type(server) is not type(Server()):
            return None, "No server was provided"
        if server.name is None or str(server.name) == "":
            return None, "No server 'name' was provided"
        elif server.hostID is None:
            return None, "No server 'hostID' was provided"
        elif server.hostImageID is None or server.hostImageID == "":
            return None, "No server 'hostImageID' was provided"
        elif server.sizeID is None or str(server.sizeID) == "":
            return None, "No server 'sizeID' was provided"
        elif server.regionID is None or str(server.regionID) == "":
            return None, "No server 'regionID' was provided"
        if type(server.hostID) != type(int()):
            return None, "Invalid server 'hostID' was provided"
        elif type(server.hostImageID) != type(str()):
            return None, "Invalid server 'hostImageID' was provided"
        if server.sshKeys is not None and type(server.sshKeys) != type(SSHKey()):
            return None, "Invalid SSH Key was provided"
        elif server.sshKeys is not None and type(server.sshKeys) == type(SSHKey()):
            if server.sshKeys.name is None or server.sshKeys.name == "":
                return None, "Invalid SSH Key 'name' was provided"
            elif server.sshKeys.content is None or server.sshKeys.content == "":
                return None, "Invalid SSH Key 'content' was provided"
        elif server.password is None or str(server.password) == "":
                return None, "No server 'sshKeys' or 'password' provided"
        
        # Store server object to be processed by BaseAPI to submit the new server to the API
        newServerParams = {
            "server": server.__dict__
        }

        # Send data to API and get response
        data = self.getData("servers", type=POST, params=newServerParams)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Show a server by the given id
    def Show(self, id = None):
        # Check if id is passed
        if id is None or id == "":
            return None, "No server 'id' was provided"

        url = "servers/{}".format(id)

        # Get data from API
        data = self.getData(url)

        # Return message response or data
        if data is not None:
            if "message" in data:
                return None, data["message"]
        
        return data, None
    
    # Destroy a server by the given id
    def Destroy(self, id = None):
        # Check if id is passed
        if id is None or id == "":
            return "No server 'id' was provided"
        
        url = "servers/{}".format(id)

        # Send DELETE request to API with given id and get response
        data = self.getData(url, type=DELETE)

        # Return message response if there is one
        if data is not None:
            if "message" in data:
                return data["message"]
        
        return None
    
    