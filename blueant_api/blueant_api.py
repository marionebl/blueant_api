from flask import Flask, request, jsonify, abort, Response
from flasgger import Swagger, swag_from
from zeep.exceptions import Fault
from .client.client import Client
from .routes.activities import activities
from .routes.customers import customers
from .routes.login import login
from .routes.projects import projects
from .routes.project_tasks import project_tasks
from .routes.times import times
from .routes.create_time import create_time
from .routes.update_time import update_time
from .exceptions import InternalServerError, Unauthorized
from .json_encoder import JSONEncoder

app = Flask(__name__)
app.config.from_object("config")

app.config['SWAGGER'] = {
    "title": "Blue Ant API",
    "version": "1.0.0",
    "uiversion": 3,
    "securityDefinitions": {
      "SessionAuth": {
          "type": "apiKey",
          "name": "X-Session-ID",
          "in": "header"
      },
      "PersonAuth": {
          "type": "apiKey",
          "name": "X-Person-ID",
          "in": "header"
      }
    }
}

swagger = Swagger(app)

app.json_encoder = JSONEncoder

@app.route("/auth/login", methods=["POST"])
@swag_from("routes/login.yml")
def login_route():
    return login()


@app.route("/activities", methods=["GET"])
@swag_from("routes/activities.yml")
def activities_route():
    return activities()


@app.route("/customers", methods=["GET"])
@swag_from("routes/customers.yml")
def customers_route():
    return customers()


@app.route("/projects", methods=["GET"])
@swag_from("routes/projects.yml")
def projects_route():
    return projects()


@app.route("/project/<string:project_id>/tasks", methods=["GET"])
@swag_from("routes/project_tasks.yml")
def project_tasks_route(project_id):
    return project_tasks(project_id)

@app.route("/times", methods=["GET"])
@swag_from("routes/times.yml")
def times_route():
    return times()

@app.route("/time", methods=["POST"])
@swag_from("routes/create_time.yml")
def create_time_route():
    return create_time()

@app.route("/time", methods=["PUT"])
@swag_from("routes/update_time.yml")
def update_time_route():
    return update_time()


@app.errorhandler(InternalServerError)
@app.errorhandler(Unauthorized)
def handle_internal_server_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
