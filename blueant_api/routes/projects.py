from flask import request, jsonify, current_app as app
from ..client.client import Client


def projects():
    client = Client(app.config['BLUEANT_API_URL'])
    client.session = dict(
        sessionID=request.headers.get('X-Session-ID'),
        personID=request.headers.get('X-Person-ID')
    )

    return jsonify(client.list_projects())