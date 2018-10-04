from zeep import CachingClient as Client
from ..common import dateparam
from ..common.util import quote

def client():
    global service
    if not 'service' in globals():
        service =  Client(config.load()['url'] + 'WorktimeAccountingService?wsdl')
    return service

def syncProjects():
    projects = {}
    for project in client().service.getProjects(sessionID()):
        projects[quote(project.name)] = {
                'id': str(project.projectID),
                'billable': project.billable}

def syncTasks():
    tasks = {}
    for projectName, x in list(projects().items()):
        tasks[projectName] = {}
        for task in client().service.getTasks(sessionID(), x['id']):
            tasks[projectName].update(extractTasks(task))

def extractTasks(task, prefix=''):
    result = {}
    if task.worktimeAllowed:
        result[quote(prefix + task.name)] = str(task.taskID)

    if task.children is not None:
        for subTask in task.children.WorkTimeTask:
            result.update(extractTasks(subTask, task.name + '__'))
    return result

def add(date, project, task, activity, billable, duration, comment):
    projectID = projects()[project]['id']
    taskID = tasks()[project][task]
    activityID = activities()[activity]

    comment = ' '.join(comment)
    with client().settings(raw_response=True):
        response = client().service.editWorktime(
            sessionID=sessionID(),
            date=dateparam.format(date[0]),
            projectID=projectID,
            taskID=taskID,
            activityID=activityID,
            duration=(float(duration) * 60 * 60),
            billable=billable,
            comment=comment,
            workTimeID=None)
        assert response.status_code == 200, 'raw_response is not 200'

def copy(from_date, workTimeID, to_date, duration):
    current = client().service.getWorktime(sessionID(), workTimeID)[0]

    with client().settings(raw_response=True):
        client().service.editWorktime(
            sessionID=sessionID(),
            date=dateparam.format(to_date[0]),
            projectID=current['projectID'],
            taskID=current['taskID'],
            activityID=current['activityID'],
            duration=(float(duration) * 60 * 60),
            billable=current['billable'],
            comment=current['comment'],
            workTimeID=None)


def delete(workTimeID, date):
    client().service.deleteWorktime(sessionID(), workTimeID)


def update(date, workTimeID, duration):
    current = client().service.getWorktime(sessionID(), workTimeID)[0]
    with client().settings(raw_response=True):
        client().service.editWorktime(
            sessionID(),
            date=current['date'],
            projectID=current['projectID'],
            comment=current['comment'],
            activityID=current['activityID'],
            taskID=current['taskID'],
            billable=current['billable'],
            workTimeID=workTimeID,
            duration=float(duration) * 60 * 60)

def move(from_date, workTimeID, to_date):
    current = client().service.getWorktime(sessionID(), workTimeID)[0]
    
    with client().settings(raw_response=True):
        client().service.editWorktime(
            sessionID(),
            date=dateparam.format(to_date[0]),
            projectID=current['projectID'],
            comment=current['comment'],
            activityID=current['activityID'],
            taskID=current['taskID'],
            billable=current['billable'],
            workTimeID=workTimeID,
            duration=float(current['duration']) / 1000)

