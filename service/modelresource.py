from flask_restful import Resource
from flask_restful import request

from service.logger import Logger
from service.models import Model
from service.errors import errors
from service.errors import Error
from service.data_format import columns


def check_user_id(user_id) -> bool:
    return isinstance(user_id, int)


def check_data(data: {}) -> bool:
    for column in columns:
        # check if column exists
        if data.get(column["name"]) is None:
            return False
        # TODO checks

    return True


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
        if not check_data(product_data):
            raise Error(errors["wrong_data"])

        # Predict
        picked_model = self.pick_model(user_id)
        result = picked_model.predict(product_data)

        # Log
        self.logger.log(picked_model, product_data, result)

        # Return result
        return {"result": result}

    def pick_model(self, user_id) -> Model:
        if user_id % 2 == 0:
            return self.simple_model
        else:
            return self.complex_model
