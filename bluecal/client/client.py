from . import baseService, humanService, masterDataService, projectsService, workTimeAccountingService

class Client:
    def __init__(self, url):
        self.url = url

    def login(self, username, password):
        return baseService.login(self, username, password)

    def logout(self, session):
        return baseService.logout(self, session)