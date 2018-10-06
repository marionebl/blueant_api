from flask import request, jsonify, current_app as app
from ..client.client import Client

def project_tasks(project_id):
    client = Client(app.config['API_URL'])
    client.session = dict(
        sessionID=request.headers.get('X-Session-ID'),
        personID=request.headers.get('X-Person-ID')
    )

    return jsonify(client.list_tasks(project_id))