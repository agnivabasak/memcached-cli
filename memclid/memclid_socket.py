import socket
import re
from .exceptions import *

class MemclidSocket:
    def __init__(self, sock=None):
        try:
            if sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.sock = sock
        except:
            raise MemclidConnectionError()

    def connect(self, host, port):
        try:
            self.host=host
            self.port=port
            self.sock.connect((host, port))
            #print("Connected to Memcached server successfully" + " (host: " + str(host) + ", port: " + str(port) +")" )
        except: 
            raise MemclidConnectionError(host,port)
    
    def disconnect(self):
        try:
            self.sock.shutdown(2) 
            """0 - disabled further recv (for cliet) ,1 - disabled further send (for client - this appln), 2 -both
            shutdown does it on a networking level by sending a FIN to server (the FIN - ACK cycle from both ends happen)"""
            self.sock.close()
            """close does the actual memory related closing of the connection on python side, also its supposed to send a TSP
            RST (RESET) response to the server"""
            self.sock = None
            #print("Disconnected from Memcached server successfully" + " (host: " + str(self.host) + ", port: " + str(self.port) +")" )
        except:
            raise MemclidDisconnectError(self.host,self.port)
    
    def send(self, msg):
        try:
            totalsent = 0
            while totalsent < len(msg):
                sent = self.sock.send(msg[totalsent:].encode())
                if sent == 0:
                    raise MemclidConnectionBreakError(self.host,self.port)
                totalsent = totalsent + sent
        except MemclidConnectionBreakError as err:
            raise err
        except:
            raise MemclidSendError(self.host,self.port)

    
    def receive(self):
        try:
            data = self.sock.recv(3072).decode()
            if len(data)==0:
                raise MemclidConnectionBreakError(self.host,self.port,"It was possibly a bad request")
            clientErrorResult = re.search("^CLIENT_ERROR\s(.*)\r\n$", data)
            serverErrorResult = re.search("^SERVER_ERROR\s(.*)\r\n$", data)
            if data=="ERROR\r\n":
                raise MemclidErrorSentByServer(self.host,self.port)
            elif clientErrorResult:
                raise MemclidClientErrorSentByServer(self.host,self.port,clientErrorResult.group(1))
            elif serverErrorResult:
                raise MemclidServerErrorSentByServer(self.host,self.port,serverErrorResult.group(1))
            return data
        except (MemclidConnectionBreakError,MemclidErrorSentByServer,MemclidClientErrorSentByServer,MemclidServerErrorSentByServer) as err:
            raise err
        except:
            raise MemclidRecvError(self.host,self.port)