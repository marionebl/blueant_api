from . import baseService, humanService, masterDataService, projectsService, workTimeAccountingService

class Client:
    def __init__(self, url):
        self.url = url
        self.session = dict(
            sessionID=None,
            personID=None
        )

    def login(self, username, password):
        data = baseService.login(self, username, password)
        self.session.update(dict(
            sessionID=data.sessionID,
            personID=data.personID
        ))
        return self.session

    def logout(self, session):
        baseService.logout(self, session)
        self.session = None

    def list_projects(self):
        return workTimeAccountingService.get_projects(self)

    def list_tasks(self, project_id):
        return workTimeAccountingService.get_tasks(self, project_id)