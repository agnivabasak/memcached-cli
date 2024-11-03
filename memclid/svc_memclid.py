import click
import re
from memclid.exceptions import *
from memclid.constants import *

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
            valueReceivedRegEx = "^VALUE\stestKey\s(\d+)\s\d+\r\n(.*)\r\nEND\r\n$"
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

    def handleAllExceptions(self,err):
        try:
            print(err)
            raise err
        except (MemclidConnectionError, MemclidDisconnectError, MemclidConnectionBreakError, MemclidSendError, MemclidRecvError, MemclidErrorSentByServer, MemclidClientErrorSentByServer, MemclidServerErrorSentByServer, MemclidUnrecognizedResponseSentByServer) as err:
            click.echo(err.message)
        except :
            click.echo("An unexpected error occured")
        finally:
            raise click.Abort()
        
