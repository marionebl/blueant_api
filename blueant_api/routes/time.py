from flask import request, jsonify, current_app as app
from zeep.exceptions import Fault
from ..client.client import Client
from ..exceptions import Unauthorized, InternalServerError
from xml.etree import ElementTree

def time(time_id):
    client = Client(app.config['API_URL'])
    client.session = dict(
        sessionID=request.headers.get('X-Session-ID'),
        personID=request.headers.get('X-Person-ID')
    )

    try:
        return jsonify(client.get_time(workTimeID=time_id))
    except Fault as error:
        error_type = error.message.split(":")[-1]
        error_type = error_type.strip() if type(error_type) is str else "Unknown"

        if error_type == "InvalidUsernamePasswordCombinationException":
            raise Unauthorized(
                error.message, payload=dict(error_type=error_type))
        else:
            raise InternalServerError(
                error.message, payload=dict(error_type=error_type))