from flask import Flask
from .client.client import Client

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def hello():
    client = Client(app.config['API_URL'])
    session = client.login(); # pass credentials here
    return "session"