from zeep import CachingClient as Client, helpers
from xmltodict import parse
from ..common import dateparam
from ..common.util import quote
from .masterDataService import syncActivities


def client(c):
    return Client(c.url + 'WorktimeAccountingService?wsdl')


def get_projects(c):
    projects = client(c).service.getProjects(
        sessionID=c.session.get('sessionID')
    )
    return list(map(lambda project: helpers.serialize_object(project), projects))


def get_tasks(c, project_id):
    tasks = client(c).service.getTasks(c.session.get('sessionID'), project_id)
    return list(map(lambda task: helpers.serialize_object(task), tasks))


def get_times(c, **params):
    times = client(c).service.getPersonalWorktime(
        sessionID=c.session.get('sessionID'),
        **params
    )
    print(times)
    return list(map(lambda time: helpers.serialize_object(time), times))


def create_time(c, **data):
    cl = client(c)

    # Access raw xml response due to https://github.com/mvantellingen/python-zeep/pull/690
    with cl.settings(raw_response=True):
        response = cl.service.editWorktime(
            sessionID=c.session.get('sessionID'),
            date=data.get('date'),
            duration=data.get('duration'),
            ticketID=data.get('ticketID'),
            projectID=data.get('projectID'),
            taskID=data.get('taskID'),
            activityID=data.get('activityID'),
            comment=data.get('comment'),
            billable=data.get('billable'),
            reasonNotAccountableID=data.get('reasonNotAccountableID'),
            iccID=data.get('iccID'),
            **{
                'from': data.get('from'),
                'to': data.get('to')
            }
        )

        data = parse(response.text)
        workTimeID = int(data['soapenv:Envelope']['soapenv:Body']['ns2:mandatoryID']['#text'])

        return get_times(c, workTimeID=workTimeID)


def syncTasks(c):
    tasks = {}
    for projectName, x in get_projects(c):
        tasks[projectName] = {}
        for task in client(c).service.getTasks(c.session.get('sessionID'), x['id']):
            tasks[projectName].update(extractTasks(task))
    return tasks


def extractTasks(task, prefix=''):
    result = {}
    if task.worktimeAllowed:
        result[quote(prefix + task.name)] = str(task.taskID)

    if task.children is not None:
        for subTask in task.children.WorkTimeTask:
            result.update(extractTasks(subTask, task.name + '__'))
    return result


def add(c, date, project, task, activity, billable, duration, comment):
    projectID = get_projects(c)[project]['id']
    taskID = syncTasks(c)[project][task]
    activityID = syncActivities(c)[activity]

    comment = ' '.join(comment)
    with client(c).settings(raw_response=True):
        response = client(c).service.editWorktime(
            sessionID=c.session.get('sessionID'),
            date=dateparam.format(date[0]),
            projectID=projectID,
            taskID=taskID,
            activityID=activityID,
            duration=(float(duration) * 60 * 60),
            billable=billable,
            comment=comment,
            workTimeID=None)
        assert response.status_code == 200, 'raw_response is not 200'


def copy(c, from_date, workTimeID, to_date, duration):
    current = client(c).service.getWorktime(
        c.session.get('sessionID'), workTimeID)[0]

    with client(c).settings(raw_response=True):
        client(c).service.editWorktime(
            sessionID=c.session.get('sessionID'),
            date=dateparam.format(to_date[0]),
            projectID=current['projectID'],
            taskID=current['taskID'],
            activityID=current['activityID'],
            duration=(float(duration) * 60 * 60),
            billable=current['billable'],
            comment=current['comment'],
            workTimeID=None)


def delete(c, workTimeID, date):
    client(c).service.deleteWorktime(c.session.get('sessionID'), workTimeID)


def update(c, date, workTimeID, duration):
    current = client(c).service.getWorktime(
        c.session.get('sessionID'), workTimeID)[0]
    with client(c).settings(raw_response=True):
        client(c).service.editWorktime(
            c.session.get('sessionID'),
            date=current['date'],
            projectID=current['projectID'],
            comment=current['comment'],
            activityID=current['activityID'],
            taskID=current['taskID'],
            billable=current['billable'],
            workTimeID=workTimeID,
            duration=float(duration) * 60 * 60)


def move(c, from_date, workTimeID, to_date):
    current = client(c).service.getWorktime(
        c.session.get('sessionID'), workTimeID)[0]

    with client(c).settings(raw_response=True):
        client(c).service.editWorktime(
            c.session.get('sessionID'),
            date=dateparam.format(to_date[0]),
            projectID=current['projectID'],
            comment=current['comment'],
            activityID=current['activityID'],
            taskID=current['taskID'],
            billable=current['billable'],
            workTimeID=workTimeID,
            duration=float(current['duration']) / 1000)