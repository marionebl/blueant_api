from zeep import CachingClient as Client, helpers
from zeep.exceptions import Fault
from xmltodict import parse


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
    return list(map(lambda time: helpers.serialize_object(time), times))


def get_time(c, **params):
    times = client(c).service.getPersonalWorktime(
        sessionID=c.session.get('sessionID'),
        workTimeID=params.get('workTimeID')
    )
    return list(map(lambda time: helpers.serialize_object(time), times))


def create_time(c, **data):
    return _edit_worktime(c, 
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


def update_time(c, **data):
    return _edit_worktime(c, 
        sessionID=c.session.get('sessionID'),
        workTimeID=int(data.get('workTimeID')),
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


def delete_time(c, **params):
    client(c).service.deleteWorktime(
        sessionID=c.session.get('sessionID'),
        workTimeID=params.get('workTimeID')
    )


def change_time_state(c, work_time_id=None, work_time_state=None):
    list_type = client(c).get_type('ns2:T_WorkTimeStateList')
    item_type = client(c).get_type('ns2:T_WorkTimeState')
    state_type = client(c).get_type('ns2:WorkTimeStateValues')

    work_time_state_list = list_type([
        item_type(
            workTimeID=work_time_id,
            state=state_type(work_time_state),
        )
    ])

    client(c).service.changeWorktimeState(
        sessionID=c.session.get('sessionID'),
        worktimeStateList=work_time_state_list
    )


def _edit_worktime(c, **data):
    cl = client(c)

    # Access raw xml response due to https://github.com/mvantellingen/python-zeep/pull/690
    with cl.settings(raw_response=True):
        response = cl.service.editWorktime(**data)
        data = parse(response.text)
        fault = data['soapenv:Envelope']['soapenv:Body']['soapenv:Fault']['faultstring'] if 'soapenv:Fault' in data['soapenv:Envelope']['soapenv:Body'] else None

        if fault is not None:
            raise Fault(fault)
        else:
            work_time_id = int(data['soapenv:Envelope']['soapenv:Body']['ns2:mandatoryID']['#text'])
            return get_times(c, workTimeID=work_time_id)
