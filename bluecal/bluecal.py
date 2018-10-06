from flask import Flask, request, jsonify, abort, Response
from flasgger import Swagger,swag_from
from zeep.exceptions import Fault
from .client.client import Client
from .routes.login import login
from .routes.projects import projects
from .exceptions import InternalServerError, Unauthorized

app = Flask(__name__)
app.config.from_object('config')

app.config['SWAGGER'] = {
    'title': 'BlueCal API',
    'uiversion': 3
}

swagger = Swagger(app)


@app.route("/auth/login", methods=["POST"])
@swag_from("routes/login.yml")
def login_route():
  return login()

@app.route("/projects", methods=["GET"])
@swag_from("routes/projects.yml")
def projects_route():
  return projects()


@app.errorhandler(InternalServerError)
@app.errorhandler(Unauthorized)
def handle_internal_server_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
