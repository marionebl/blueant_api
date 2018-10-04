from flask import Flask, request, jsonify
from .client.client import Client

app = Flask(__name__)
app.config.from_object('config')


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    client = Client(app.config['API_URL'])
    session = client.login(username, password)

    return jsonify(
        sessionID=session.sessionID,
        personID=session.personID
    )
