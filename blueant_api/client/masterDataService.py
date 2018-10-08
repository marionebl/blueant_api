from zeep import CachingClient as Client, helpers
from ..common.util import quote


def client(c):
    return Client(c.url + 'MasterDataService?wsdl')


def get_activities(c):
    activities = client(c).service.getActivities(
        sessionID=c.session.get('sessionID'),
        defaultvalue=False
    )
    return list(map(lambda activity: helpers.serialize_object(activity), activities))


def syncActivities(c):
    raw_activities = client(c).service.getActivities(
            sessionID=c.session.sessionID,
            defaultvalue=False)

    activities = {}
    for activity in [x for x in raw_activities if x.active]:
        activities[quote(activity.name)] = str(activity.activityID)


def get_customers(c):
    customers = client(c).service.searchCustomer(
        sessionID=c.session.get('sessionID')
    )
    return list(map(lambda customer: helpers.serialize_object(customer), customers))