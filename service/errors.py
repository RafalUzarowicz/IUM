errors = {
    "wrong_user_id": {"message": "Wrong user id", "code": 400},
    "wrong_data_type": {"message": "Wrong data type", "code": 415},
    "missing_json_data": {"message": "Missing json", "code": 422},
    "wrong_data": {"message": "Wrong data", "code": 422}
}


class Error(Exception):
    status_code = 400

    def __init__(self, error: {}, payload=None):
        Exception.__init__(self)
        self.message = error["message"]
        if error.get("code") is not None:
            self.status_code = error["code"]
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
