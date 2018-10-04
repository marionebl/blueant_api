from flask import Flask, request, jsonify
from .client.client import Client

app = Flask(__name__)
app.config.from_object('config')


@app.route("/login", methods=["POST"])
def login():
    json = request.get_json()
    data = request.form if json is None else json;

    username = data.get("username")
    password = data.get("password")

    client = Client(app.config['API_URL'])
    session = client.login(username, password)

    return jsonify(
        sessionID=session.sessionID,
        personID=session.personID
    )
