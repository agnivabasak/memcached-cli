import click
import re
from .exceptions import *
from .constants import *

class MemclidUtility:
    def __init__(self, memclidSocket):
        self.sock = memclidSocket
    
    def get(self,key):
        try:
            finalResult = {
                "flag": None,
                "value": None,
                "message": "",
                "status": ""
            }
            msg = "get "+key+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            valueReceivedRegEx = "^VALUE\s"+key+"\s(\d+)\s\d+\r\n(.*)\r\nEND\r\n$"
            valueNotReceivedRegEx = "^END\r\n$"
            valueReceivedResult = re.search(valueReceivedRegEx,data)
            valueNotReceivedResult = re.search(valueNotReceivedRegEx,data)
            if valueReceivedResult:
                finalResult["flag"]=valueReceivedResult.group(1)
                finalResult["value"]=valueReceivedResult.group(2)
                finalResult["message"]="Fetched the value for "+key
                finalResult["status"]=STATUS_DATA_AVAILABLE
            elif valueNotReceivedResult:
                finalResult["status"]=STATUS_DATA_NOT_AVAILABLE
                finalResult["message"]="No value found for "+key
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def set(self,key,value,flag,exptime):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "set "+key+" "+str(flag)+" "+str(exptime)+" "+str(len(value))+"\r\n"+value+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^STORED\r\n$"
            notStoredRegex = "^NOT_STORED\r\n$"
            storedResult = re.search(storedRegex,data)
            notStoredResult = re.search(notStoredRegex,data)
            if storedResult:
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The data was saved successfully"
            elif notStoredResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The data could not be stored"
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def add(self,key,value,flag,exptime):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "add "+key+" "+str(flag)+" "+str(exptime)+" "+str(len(value))+"\r\n"+value+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^STORED\r\n$"
            notStoredRegex = "^NOT_STORED\r\n$"
            storedResult = re.search(storedRegex,data)
            notStoredResult = re.search(notStoredRegex,data)
            if storedResult:
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The data was saved successfully"
            elif notStoredResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The record is already stored in memcached server. It could not be stored due to the preconditions of the command executed."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def replace(self,key,value,flag,exptime):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "replace "+key+" "+str(flag)+" "+str(exptime)+" "+str(len(value))+"\r\n"+value+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^STORED\r\n$"
            notStoredRegex = "^NOT_STORED\r\n$"
            storedResult = re.search(storedRegex,data)
            notStoredResult = re.search(notStoredRegex,data)
            if storedResult:
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The value for the key was replaced successfully"
            elif notStoredResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The key doesnt exist in the memcached server. It could not be stored due to the preconditions of the command executed."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def append(self,key,value):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "append "+key+" 0 3600 "+str(len(value))+"\r\n"+value+"\r\n" 
            #the flag and exptime aren't changed by append but they are still required when sending the request
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^STORED\r\n$"
            notStoredRegex = "^NOT_STORED\r\n$"
            storedResult = re.search(storedRegex,data)
            notStoredResult = re.search(notStoredRegex,data)
            if storedResult:
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The value was appended successfully"
            elif notStoredResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The key most likely doesnt exist in the memcached server. It could not be stored."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def prepend(self,key,value):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "prepend "+key+" 0 3600 "+str(len(value))+"\r\n"+value+"\r\n" 
            #the flag and exptime aren't changed by append but they are still required when sending the request
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^STORED\r\n$"
            notStoredRegex = "^NOT_STORED\r\n$"
            storedResult = re.search(storedRegex,data)
            notStoredResult = re.search(notStoredRegex,data)
            if storedResult:
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The value was prepended successfully"
            elif notStoredResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The key most likely doesnt exist in the memcached server. It could not be stored."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def gets(self,key):
        try:
            finalResult = {
                "flag": None,
                "value": None,
                "cas_unique": None,
                "message": "",
                "status": ""
            }
            msg = "gets "+key+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            valueReceivedRegEx = "^VALUE\s"+key+"\s(\d+)\s\d+\s(\d+)\r\n(.*)\r\nEND\r\n$"
            valueNotReceivedRegEx = "^END\r\n$"
            valueReceivedResult = re.search(valueReceivedRegEx,data)
            valueNotReceivedResult = re.search(valueNotReceivedRegEx,data)
            if valueReceivedResult:
                finalResult["flag"]=valueReceivedResult.group(1)
                finalResult["value"]=valueReceivedResult.group(3)
                finalResult["cas_unique"]=valueReceivedResult.group(2)
                finalResult["message"]="Fetched the value for "+key
                finalResult["status"]=STATUS_DATA_AVAILABLE
            elif valueNotReceivedResult:
                finalResult["status"]=STATUS_DATA_NOT_AVAILABLE
                finalResult["message"]="No value found for "+key
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def cas(self,key,value,cas_unique,flag,exptime):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "cas "+key+" "+str(flag)+" "+str(exptime)+" "+str(len(value))+" "+str(cas_unique)+"\r\n"+value+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^STORED\r\n$"
            existsRegex = "^EXISTS\r\n$"
            notFoundRegex = "^NOT_FOUND\r\n$"
            storedResult = re.search(storedRegex,data)
            existsResult = re.search(existsRegex,data)
            notFoundResult = re.search(notFoundRegex,data)
            if storedResult:
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The value for the key was set successfully"
            elif existsResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The value was modified since it was last fetched. It could not be stored due to the preconditions of the command executed."
            elif notFoundResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The key doesnt exist in the memcached server. It could not be stored due to the preconditions of the command executed."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def delete(self,key):
        try:
            finalResult = {
                "message": "",
                "status": ""
            }
            msg = "delete "+key+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            deletedRegex = "^DELETED\r\n$"
            notFoundRegex = "^NOT_FOUND\r\n$"
            deletedResult = re.search(deletedRegex,data)
            notFoundResult = re.search(notFoundRegex,data)
            if deletedResult:
                finalResult["status"]=STATUS_RECORD_DELETED
                finalResult["message"]="The data was deleted successfully"
            elif notFoundResult:
                finalResult["status"]=STATUS_RECORD_NOT_DELETED
                finalResult["message"]="The record was not found in the memcached server. It could not be deleted due to the preconditions of the command executed."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)
    
    def incr(self,key,value):
        try:
            finalResult = {
                "updated_value": None,
                "message": "",
                "status": ""
            }
            msg = "incr "+key+" "+str(value)+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^(\d+)\r\n$"
            notFoundRegex = "^NOT_FOUND\r\n$"
            storedResult = re.search(storedRegex,data)
            notFoundResult = re.search(notFoundRegex,data)
            if storedResult:
                finalResult["updated_value"]=storedResult.group(1)
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The value for the key was incremented successfully"
            elif notFoundResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The key doesnt exist in the memcached server. It could not be incremented due to the preconditions of the command executed."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def decr(self,key,value):
        try:
            finalResult = {
                "updated_value": None,
                "message": "",
                "status": ""
            }
            msg = "decr "+key+" "+str(value)+"\r\n"
            self.sock.send(msg)
            data = self.sock.receive()
            storedRegex = "^(\d+)\r\n$"
            notFoundRegex = "^NOT_FOUND\r\n$"
            storedResult = re.search(storedRegex,data)
            notFoundResult = re.search(notFoundRegex,data)
            if storedResult:
                finalResult["updated_value"]=storedResult.group(1)
                finalResult["status"]=STATUS_RECORD_STORED
                finalResult["message"]="The value for the key was decremented successfully"
            elif notFoundResult:
                finalResult["status"]=STATUS_RECORD_NOT_STORED
                finalResult["message"]="The key doesnt exist in the memcached server. It could not be decremented due to the preconditions of the command executed."
            else:
                raise MemclidUnrecognizedResponseSentByServer(self.sock.host,self.sock.port,data)
            return finalResult
        except Exception as err:
            self.handleAllExceptions(err)

    def handleAllExceptions(self,err):
        try:
            raise err
        except (MemclidConnectionError, MemclidDisconnectError, MemclidConnectionBreakError, MemclidSendError, MemclidRecvError, MemclidErrorSentByServer, MemclidClientErrorSentByServer, MemclidServerErrorSentByServer, MemclidUnrecognizedResponseSentByServer) as err:
            click.echo(err.message)
        except :
            click.echo("An unexpected error occured")
        finally:
            raise click.Abort()
        
