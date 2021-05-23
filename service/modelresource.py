from flask_restful import Resource
from flask_restful import request
import pandas as pd

from service.logger import Logger
from service.models import Model
from service.errors import errors
from service.errors import Error
from service.data_format import columns


def check_user_id(user_id) -> bool:
    return isinstance(user_id, int) and user_id >= 0


def check_data(data: {}) -> {}:
    if data is None or not isinstance(data, dict):
        return errors["wrong_data"]

    for column in columns:
        # Check if column exists
        if data.get(column["name"]) is None:
            return errors["wrong_columns"]

    # Check purchase timestamp
    if pd.to_datetime(data["purchase_timestamp"], format='%Y-%m-%dT%H:%M', errors="coerce") is pd.NaT:
        return errors["wrong_purchase_timestamp"]
    # Check delivery company
    try:
        tmp = int(data["delivery_company"])
        if tmp < 0:
            return errors["wrong_delivery_company"]
    except ValueError:
        return errors["wrong_delivery_company"]
    # Check product id
    try:
        tmp = int(data["product_id"])
        if tmp < 0:
            return errors["wrong_product_id"]
    except ValueError:
        return errors["wrong_product_id"]
    # Check price
    try:
        tmp = float(data["price"])
        if tmp < 0:
            return errors["wrong_price"]
    except ValueError:
        return errors["wrong_price"]
    # Check offered discount
    try:
        tmp = int(data["offered_discount"])
        if tmp < 0:
            return errors["wrong_offered_discount"]
    except ValueError:
        return errors["wrong_offered_discount"]
    # Check street
    street = str(data["street"]).split(" ")
    if len(street) < 3:
        return errors["wrong_street"]
    number = street[-1].split("/")
    try:
        for num in number:
            int(num)
    except ValueError:
        return errors["wrong_street_number"]

    return None


class ModelResource(Resource):
    def __init__(self, simple_model: Model, complex_model: Model, logger: Logger):
        super()
        self.logger = logger
        self.simple_model = simple_model
        self.complex_model = complex_model

    def get(self, user_id):
        # Check user id
        if not check_user_id(user_id):
            raise Error(errors["wrong_user_id"])

        # Check request data type
        if not request.is_json:
            raise Error(errors["wrong_data_type"])

        # Get data
        product_data = request.get_json()
        if product_data is None:
            raise Error(errors["missing_json_data"])

        # Validate data
        check_data_result = check_data(product_data)
        if check_data_result is not None:
            raise Error(check_data_result)

        # Predict
        picked_model = self.pick_model(user_id)
        result = picked_model.predict(product_data)

        # Log
        self.logger.log(picked_model, product_data, result)

        # Return result
        return {"result": result}

    def pick_model(self, user_id) -> Model:
        # Pick model based on user id
        if user_id % 2 == 0:
            return self.simple_model
        else:
            return self.complex_model
