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
