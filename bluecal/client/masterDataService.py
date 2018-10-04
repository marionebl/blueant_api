from zeep import CachingClient as Client
from ..common.util import quote

def client():
    return Client(config.load()['url'] + 'MasterDataService?wsdl')

def syncActivities():
    raw_activities = client().service.getActivities(
            sessionID=sessionID(),
            defaultvalue=False)

    activities = {}
    for activity in [x for x in raw_activities if x.active]:
        activities[quote(activity.name)] = str(activity.activityID)
