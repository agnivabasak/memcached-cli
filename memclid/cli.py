import click

from .exceptions import MemclidConnectionError, MemclidDisconnectError
from .config import DEFAULT_MEMCLID_HOST, DEFAULT_MEMCLID_PORT
from .memclid_socket import MemclidSocket
from .svc_memclid import MemclidUtility
from .constants import *

class Context:
    #Defining a context manager (anything with __enter__ and __exit__ defined)
    def __init__(self,host=None,port=None): #Called when the object is created
        self.MEMCLID_HOST = host or DEFAULT_MEMCLID_HOST
        self.MEMCLID_PORT = port or DEFAULT_MEMCLID_PORT
    def __enter__(self): #Called when the  object is used with the "with" statement
        try:
            self.MEMCLID_SOCKET = MemclidSocket()
            self.MEMCLID_SOCKET.connect(self.MEMCLID_HOST,self.MEMCLID_PORT)
            self.MEMCLID_UTILITY = MemclidUtility(self.MEMCLID_SOCKET)
        except MemclidConnectionError as err:
            click.echo(err.message)
            raise click.Abort()
        except :
            click.echo("An unexpected error occured")
            raise click.Abort()
        return self
    def __exit__(self, exc_type, exc_value, tb):
        try:
            self.MEMCLID_SOCKET.disconnect()
        except MemclidDisconnectError as err:
            click.echo(err.message)
            raise click.Abort()
        except :
            click.echo("An unexpected error occured")
            raise click.Abort()

@click.group()
@click.option("-h","--host", type=str, help="Host of memcached server (default is localhost)")
@click.option("-p","--port", type=int, help="Port of memcached server (default is 11211)")
@click.pass_context
def cli(ctx,host,port):
    """
    Welcome to Memclid

    A CLI tool for your memcached server
    """
    ctx.obj = ctx.with_resource(Context(host,port))

@cli.command()
@click.argument("key",type=str)
@click.pass_context
def get(ctx,key):
    """Get the value corresponding to a key stored in memcached server"""
    result = ctx.obj.MEMCLID_UTILITY.get(key)
    if result["status"] == STATUS_DATA_AVAILABLE:
        click.echo(result["message"])
        click.echo()
        click.echo(f'Value:  {result["value"]}')
        click.echo(f'Flag/Metadata:  {result["flag"]}')
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=str,default="")
@click.option("-f","--flag",type=int,default=0,help="flag/metadata to be stored along with the value (default is 0)")
@click.option("-et","--exptime",type=int,default=3600,help="expiry time in seconds for the records (default is 3600 = 1 hour)")
@click.pass_context
def set(ctx,key,value,flag,exptime):
    """Set the value corresponding to a key stored in memcached server"""
    result = ctx.obj.MEMCLID_UTILITY.set(key,value,flag,exptime)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])