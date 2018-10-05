from flask import Flask, request, jsonify, abort, Response
from flasgger import Swagger
from .client.client import Client
from zeep.exceptions import Fault

app = Flask(__name__)
app.config.from_object('config')

app.config['SWAGGER'] = {
    'title': 'BlueCal API',
    'uiversion': 3
}

swagger = Swagger(app)


@app.route("/auth/login", methods=["POST"])
def login():
    """Log in to BlueAnt by providing username and password.
    Will yield a session id that can be used to authenticate other requests.
    ---
    tags:
      - Authentication
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
        format: password
    definitions:
      Session:
        type: object
        properties:
          sessionID:
            type: string
          persionID:
            type: string
      Error:
        type: object
        properties:
          error_type:
            type: string
          message:
            type: string
    responses:
      200:
        description: A session consisting of an ID and a user reference obtained by successful login
        schema:
          $ref: '#/definitions/Session'
        examples:
          Session: { "personID": 69689598, "sessionID": "UXx6XRaM2qmUQPqcvygl" }
      401:
        description: An error indicating a wrong username password comination
        schema:
          $ref: '#/definitions/Error'
        examples:
          Error: { "error_type": "InvalidUsernamePasswordCombinationException", "message": "net.proventis.axis.blueant.InvalidUsernamePasswordCombinationException: InvalidUsernamePasswordCombinationException" }
      500:
        description: An generic server error
        schema:
          $ref: '#/definitions/Error'
        examples:
          Error: { "error_type": "Generic", "message": "Something went horribly wrong" }
    """
    json = request.get_json()
    data = request.form if json is None else json

    username = data.get("username")
    password = data.get("password")

    client = Client(app.config['API_URL'])

    try:
        session = client.login(username, password)

        return jsonify(
            sessionID=session.sessionID,
            personID=session.personID
        )
    except Fault as error:
        error_type = error.message.split(":")[-1]
        error_type = error_type.strip() if type(error_type) is str else "Unknown"

        if error_type == "InvalidUsernamePasswordCombinationException":
            raise Unauthorized(error.message, payload=dict(error_type=error_type))
        else:
            raise InternalServerError(error.message, payload=dict(error_type=error_type))

class JSONException(Exception):
    status_code = 500

    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class Unauthorized(JSONException):
    status_code = 401

    def __init__(self, message, payload=None):
        JSONException.__init__(self, message, payload=payload)


class InternalServerError(JSONException):
    status_code = 500

    def __init__(self, message, payload=None):
        JSONException.__init__(self, message, payload=payload)


@app.errorhandler(InternalServerError)
@app.errorhandler(Unauthorized)
def handle_internal_server_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
