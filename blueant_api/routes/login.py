from flask import request, jsonify, current_app as app
from zeep.exceptions import Fault
from ..client.client import Client
from ..exceptions import Unauthorized, InternalServerError


def login():
    json = request.get_json()
    data = request.form if json is None else json

    username = data.get("username")
    password = data.get("password")

    client = Client(app.config['API_URL'])

    try:
        session = client.login(username, password)

        return jsonify(
            sessionID=session.get("sessionID"),
            personID=session.get("personID")
        )
    except Fault as error:
        error_type = error.message.split(":")[-1]
        error_type = error_type.strip() if type(error_type) is str else "Unknown"

        if error_type == "InvalidUsernamePasswordCombinationException":
            raise Unauthorized(
                error.message, payload=dict(error_type=error_type))
        else:
            raise InternalServerError(
                error.message, payload=dict(error_type=error_type))