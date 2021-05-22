from typing import Type

from flask_restful import Resource
from flask_restful import request

from src.service.logger import Logger
from src.service.models import Model
from src.service.errors import error_messages
from src.service.data_format import columns


class ModelResource(Resource):
    def __init__(self, simple_model: Model, complex_model: Model, logger: Logger):
        super()
        self.logger = logger
        # Load models
        self.simple_model = simple_model
        self.complex_model = complex_model

    def get(self, user_id):
        # Check user id
        if not self.check_user_id(user_id):
            return {"error": error_messages["wrong_user_id"]}

        # Check request data type
        if not request.is_json:
            return {"error": error_messages["wrong_data_type"]}

        # Get data
        product_data = request.get_json()
        if product_data is None:
            return {"error": error_messages["missing_json_data"]}

        # Validate data
        if not self.check_data(product_data):
            return {"error": error_messages["wrong_data"]}

        # Predict
        picked_model = self.pick_model(user_id)
        result = picked_model.predict(product_data)

        # Log
        self.logger.log("", picked_model, product_data, result)

        # Return result
        return {"result": result}

    def check_data(self, data: {}) -> bool:
        for column in columns:
            # check if column exists
            if data.get(column["name"]) is None:
                return False
            # TODO checks

        return True

    def check_user_id(self, user_id) -> bool:
        return isinstance(user_id, int)

    def pick_model(self, user_id) -> Model:
        if user_id % 2 == 0:
            return self.simple_model
        else:
            return self.complex_model
