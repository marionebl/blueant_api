from flask import request, jsonify, current_app as app
from ..client.client import Client


def times():
    client = Client(app.config['API_URL'])
    client.session = dict(
        sessionID=request.headers.get('X-Session-ID'),
        personID=request.headers.get('X-Person-ID')
    )

    return jsonify(client.list_times(
        workTimeID=request.args.get('workTimeID'),
        fromDate=request.args.get('fromDate'),
        toDate=request.args.get('toDate'),
        projectID=request.args.get('projectID'),
        taskID=request.args.get('taskID'),
        state=request.args.get('state'),
        billable=request.args.get('billable'),
        reasonNotAccountableID=request.args.get('reasonNotAccountableID'),
        exported=request.args.get('exported'),
        exportStartDate=request.args.get('exportStartDate'),
        exportEndDate=request.args.get('exportEndDate')
    ))
