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

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=str,default="")
@click.option("-f","--flag",type=int,default=0,help="flag/metadata to be stored along with the value (default is 0)")
@click.option("-et","--exptime",type=int,default=3600,help="expiry time in seconds for the records (default is 3600 = 1 hour)")
@click.pass_context
def add(ctx,key,value,flag,exptime):
    """
    Add the value corresponding to a new key in memcached server

    This command won't work if a record for the Key is already stored in the memcached server
    """
    result = ctx.obj.MEMCLID_UTILITY.add(key,value,flag,exptime)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=str,default="")
@click.option("-f","--flag",type=int,default=0,help="flag/metadata to be stored along with the value (default is 0)")
@click.option("-et","--exptime",type=int,default=3600,help="expiry time in seconds for the records (default is 3600 = 1 hour)")
@click.pass_context
def replace(ctx,key,value,flag,exptime):
    """
    Replace the value corresponding to an existing key stored in memcached server

    This command won't work if a record for the Key doesn't already exist in the memcached server
    """
    result = ctx.obj.MEMCLID_UTILITY.replace(key,value,flag,exptime)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=str,default="")
@click.pass_context
def append(ctx,key,value):
    """
    Append the value to the value corresponding to an existing key stored in memcached server

    This command won't work if a record for the Key doesn't already exist in the memcached server
    """
    result = ctx.obj.MEMCLID_UTILITY.append(key,value)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=str,default="")
@click.pass_context
def prepend(ctx,key,value):
    """
    Prepend the value to the value corresponding to an existing key stored in memcached server

    This command won't work if a record for the Key doesn't already exist in the memcached server
    """
    result = ctx.obj.MEMCLID_UTILITY.prepend(key,value)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.pass_context
def gets(ctx,key):
    """Get the cas unique value for the entry and the value corresponding to a key stored in memcached server"""
    result = ctx.obj.MEMCLID_UTILITY.gets(key)
    if result["status"] == STATUS_DATA_AVAILABLE:
        click.echo(result["message"])
        click.echo()
        click.echo(f'Value:  {result["value"]}')
        click.echo(f'Flag/Metadata:  {result["flag"]}')
        click.echo(f'CAS Unique Value:  {result["cas_unique"]}')
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("cas_unique",type=int)
@click.argument("key",type=str)
@click.argument("value",type=str,default="")
@click.option("-f","--flag",type=int,default=0,help="flag/metadata to be stored along with the value (default is 0)")
@click.option("-et","--exptime",type=int,default=3600,help="expiry time in seconds for the records (default is 3600 = 1 hour)")
@click.pass_context
def cas(ctx,cas_unique,key,value,flag,exptime):
    """
    Set the value corresponding to an existing key stored in memcached server using cas_unique
    
    It works given that the value was not modified since it was last fetched

    This can be checked using the cas_unique number that can be fetched using the gets command

    This command won't work if a record for the Key doesn't already exist in the memcached server
    """
    result = ctx.obj.MEMCLID_UTILITY.cas(key,value,cas_unique,flag,exptime)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.pass_context
def delete(ctx,key):
    """Deletes the key-value stored in memcached server"""
    result = ctx.obj.MEMCLID_UTILITY.delete(key)
    if result["status"] == STATUS_RECORD_DELETED:
        click.echo(result["message"])
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=int,default=0)
@click.pass_context
def incr(ctx,key,value):
    """
    Increment the value corresponding to an existing key stored in memcached server by the value specified by the user

    This command won't work if a record for the Key doesn't already exist in the memcached server

    This command also won't work if the existing value is not of Integer type
    """
    result = ctx.obj.MEMCLID_UTILITY.incr(key,value)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
        click.echo()
        click.echo(f'Updated Value:  {result["updated_value"]}')
    else:
        click.echo(result["message"])

@cli.command()
@click.argument("key",type=str)
@click.argument("value",type=int,default=0)
@click.pass_context
def decr(ctx,key,value):
    """
    Decrement the value corresponding to an existing key stored in memcached server by the value specified by the user

    This command won't work if a record for the Key doesn't already exist in the memcached server

    This command also won't work if the existing value is not of Integer type
    """
    result = ctx.obj.MEMCLID_UTILITY.decr(key,value)
    if result["status"] == STATUS_RECORD_STORED:
        click.echo(result["message"])
        click.echo()
        click.echo(f'Updated Value:  {result["updated_value"]}')
    else:
        click.echo(result["message"])