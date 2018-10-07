from flask import Flask, request, jsonify, abort, Response, current_app as app
from flasgger import Swagger
from zeep.exceptions import Fault
from ..client.client import Client
from ..exceptions import Unauthorized, InternalServerError

def create_time():
    client = Client(app.config['API_URL'])
    client.session = dict(
        sessionID=request.headers.get('X-Session-ID'),
        personID=request.headers.get('X-Person-ID')
    )

    json = request.get_json()
    data = request.form if json is None else json

    # TODO: Check how to use flasgger to validate incoming data

    try:
        time = client.create_time(
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

        return jsonify(time)
    except Fault as error:
        error_type = error.message.split(":")[-1]
        error_type = error_type.strip() if type(error_type) is str else "Unknown"

        if error_type == "InvalidUsernamePasswordCombinationException":
            raise Unauthorized(
                error.message, payload=dict(error_type=error_type))
        else:
            raise InternalServerError(
                error.message, payload=dict(error_type=error_type))