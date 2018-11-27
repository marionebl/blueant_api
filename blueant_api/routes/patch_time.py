from flask import request, jsonify, current_app as app, abort
from zeep.exceptions import Fault
from jsonpatch import apply_patch
from xml.etree import ElementTree

from ..client.client import Client
from ..exceptions import Unauthorized, InternalServerError


def patch_time(time_id):
    try:
        client = Client(app.config['BLUEANT_API_URL'])

        client.session = dict(
            sessionID=request.headers.get('X-Session-ID'),
            personID=request.headers.get('X-Person-ID')
        )

        work_time = client.get_time(
            workTimeID=time_id
        )

        patch = request.get_json()
        patched = apply_patch(work_time, patch)

        client.change_time_state(
            work_time_id=time_id,
            work_time_state=patched.get('state')
        )

        return jsonify(patched)
    except Fault as error:
        error_type = error.message.split(":")[-1]

        if error_type == "InvalidUsernamePasswordCombinationException":
            raise Unauthorized(
                error.message, payload=dict(error_type=error_type))
        else:
            raise InternalServerError(
                error.message, payload=dict(error_type=error_type))