class MemclidConnectionError(Exception):
    """Exception raised when memclid can't connect to the memcached server

    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, message="Couldn't connect to the memcached server"):
        self.message = message;
        if host!=None and port!=None :
            self.message = message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidDisconnectError(Exception):
    """Exception raised when memclid can't disconnect from the memcached server

    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, message="Couldn't disconnect from the memcached server"):
        self.message = message;
        if host!=None and port!=None :
            self.message = message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidConnectionBreakError(Exception):
    """Exception raised when memclid's connection to the memcache server broke unexpectedly

    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        helperMessage -- more detailed error message that explains the possible reason for the failure
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, helperMessage ="", message="Connection to the Memcached server broke unexpectedly"):
        self.message = message;
        if helperMessage!= "":
            self.message = self.message + ". " + helperMessage
        if host!=None and port!=None :
            self.message = self.message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidSendError(Exception):
    """Exception raised when memclid couldnt send bytes to the memcached server successfully

    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, message="Couldn't send the request to the memcached server successfully"):
        self.message = message;
        if host!=None and port!=None :
            self.message = message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidRecvError(Exception):
    """Exception raised when memclid faced issues while receiving data from the memcached server successfully

    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, message="Faced unexpected error while receiving response from the memcached server"):
        self.message = message;
        if host!=None and port!=None :
            self.message = message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidErrorSentByServer(Exception):
    """Exception raised when the memcached server returns with "ERROR\r\n"
    which indicates that the command sent by the client(memclid) was incorrect
    
    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, message="Memcached server returned with ERROR. This happens when a nonexistent command was sent to the server."):
        self.message = message;
        if host!=None and port!=None :
            self.message = message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidClientErrorSentByServer(Exception):
    """Exception raised when the memcached server returns with "CLIENT_ERROR <message>\r\n"
    which indicates that the input request doesn't conform to the protocol in some way
    
    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        messageSentByServer -- Error message sent by the memcached server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, messageSentByServer="", message="Memcached server returned with CLIENT_ERROR. This happens when the input request doesn't conform to the protocol in some way."):
        self.message = message;
        if messageSentByServer!="" and messageSentByServer!=None:
            self.message = self.message + " Error message sent by server: " + messageSentByServer
        if host!=None and port!=None :
            self.message = self.message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidServerErrorSentByServer(Exception):
    """Exception raised when the memcached server returns with "SERVER_ERROR <message>\r\n"
    which indicates that there was a server error that prevented the server from carrying out the command
    
    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        messageSentByServer -- Error message sent by the memcached server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, messageSentByServer="", message="Memcached server returned with CLIENT_ERROR. This happens when there is a server error that prevents the server from carrying out a command."):
        self.message = message;
        if messageSentByServer!="" and messageSentByServer!=None:
            self.message = self.message + " Error message sent by server: " + messageSentByServer
        if host!=None and port!=None :
            self.message = self.message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)

class MemclidUnrecognizedResponseSentByServer(Exception):
    """Exception raised when the memcached server returns with a response
    that doesnt match the expected responses
    
    Attributes:
        host -- host of the memcache server
        port -- port of the memcache server
        responseSentByServer -- response sent by the memcached server
        message -- explanation of the error
    """

    def __init__(self, host=None, port=None, responseSentByServer="", message="Memcached server returned with an unrecognized response format."):
        self.message = message;
        if responseSentByServer!="" and responseSentByServer!=None:
            self.message = self.message + " Response sent by server: " + responseSentByServer
        if host!=None and port!=None :
            self.message = self.message + " (host: " + str(host) + ", port: " + str(port) +")" 
        super().__init__(self.message)