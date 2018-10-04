from zeep import CachingClient as Client

def client():
    return Client(config.load()['url'] + 'HumanService?wsdl')
