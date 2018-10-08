from . import baseService, masterDataService, workTimeAccountingService


class Client:
    def __init__(self, url):
        self.url = url
        self.session = dict(
            sessionID=None,
            personID=None
        )

    def create_time(self, **data):
        return workTimeAccountingService.create_time(self, **data)

    def delete_time(self, **params):
        return workTimeAccountingService.delete_time(self, **params)

    def get_time(self, **params):
        times = workTimeAccountingService.get_time(self, **params)
        return times[0]

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

    def list_activities(self):
        return masterDataService.get_activities(self)

    def list_customers(self):
        return masterDataService.get_customers(self)

    def list_projects(self):
        return workTimeAccountingService.get_projects(self)

    def list_tasks(self, project_id):
        return workTimeAccountingService.get_tasks(self, project_id)

    def list_times(self, **params):
        return workTimeAccountingService.get_times(self, **params)

    def update_time(self, **data):
        return workTimeAccountingService.update_time(self, **data)
