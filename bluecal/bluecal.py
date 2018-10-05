from flask import Flask, request, jsonify
from flasgger import Swagger
from .client.client import Client

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
    responses:
      200:
        description: A session consisting of an ID and a user reference
        schema:
          $ref: '#/definitions/Session'
        examples:
          Session: { "personID": 69689598, "sessionID": "UXx6XRaM2qmUQPqcvygl" }
    """
    json = request.get_json()
    data = request.form if json is None else json

    username = data.get("username")
    password = data.get("password")

    client = Client(app.config['API_URL'])
    session = client.login(username, password)

    return jsonify(
        sessionID=session.sessionID,
        personID=session.personID
    )
