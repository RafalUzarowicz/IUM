from flask import Flask, jsonify
from flask_restful import Api

from constants import COMPLEX_MODEL_NAME, SIMPLE_MODEL_NAME, FLASK_APPLICATION_NAME
from service.errors import Error
from service.logger import Logger
from service.modelresource import ModelResource
from service.models import Model

app = Flask(FLASK_APPLICATION_NAME)
api = Api(app)

# TODO tutaj uzupelnij modele <3
simple_m = Model(SIMPLE_MODEL_NAME, "")
complex_m = Model(COMPLEX_MODEL_NAME, "")
logger = Logger()


@app.errorhandler(Error)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


api.add_resource(ModelResource, "/model", "/model/user/<int:user_id>", endpoint="models",
                 resource_class_kwargs={"simple_model": simple_m, "complex_model": complex_m, "logger": logger})