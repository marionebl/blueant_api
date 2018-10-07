from functools import wraps
from zeep import CachingClient as Client
from zeep.exceptions import Fault

def client(c):
    return Client(c.url + 'BaseService?wsdl')

def login(c, username, password):
    return client(c).service.Login(username, password)

def logout(c, sessionId):
    client(c).service.Logout(sessionId)
