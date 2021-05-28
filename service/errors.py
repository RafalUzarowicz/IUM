errors = {
    "wrong_user_id": {"message": "Wrong user id.", "code": 400},
    "wrong_data_type": {"message": "Wrong data type.", "code": 415},
    "missing_json_data": {"message": "Missing json.", "code": 422},
    "wrong_data": {"message": "Wrong data.", "code": 422},
    "wrong_columns": {"message": "Wrong columns.", "code": 422},
    "wrong_purchase_timestamp": {"message": "Purchase timestamp in wrong format.", "code": 422},
    "wrong_delivery_company": {"message": "Delivery company is not int.", "code": 422},
    "wrong_product_id": {"message": "product id is not int.", "code": 422},
    "wrong_price": {"message": "Price is not float.", "code": 422},
    "wrong_offered_discount": {"message": "Offered discount is not int.", "code": 422},
    "wrong_street": {"message": "Street in wrong format.", "code": 422},
    "wrong_street_number": {"message": "Street number is in wrong format.", "code": 422},
    "wrong_log_num": {"message": "Wrong logs number.", "code": 400},
    "wrong_model_name": {"message": "Wrong model name.", "code": 400},
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
