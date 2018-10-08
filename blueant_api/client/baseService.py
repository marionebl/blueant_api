from zeep import CachingClient as Client


def client(c):
    return Client(c.url + 'BaseService?wsdl')


def login(c, username, password):
    return client(c).service.Login(username, password)


def logout(c, session_id):
    client(c).service.Logout(session_id)
