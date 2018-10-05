from zeep import CachingClient as Client
from ..common.util import quote

def client(c):
    return Client(c.url + 'MasterDataService?wsdl')

def syncActivities(c):
    raw_activities = client(c).service.getActivities(
            sessionID=c.session.sessionID,
            defaultvalue=False)

    activities = {}
    for activity in [x for x in raw_activities if x.active]:
        activities[quote(activity.name)] = str(activity.activityID)
