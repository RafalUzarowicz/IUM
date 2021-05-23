#TODO:
# -testy
# -moze poprawic te errory ale nie wiem czy jest sens
# -pousuwac magiczne stale?

from flask import Flask, jsonify
from flask_restful import Api

from constants import HOST, PORT, MAXIMUM_LOGS_NUMBER, COMPLEX_MODEL_NAME, SIMPLE_MODEL_NAME
from service.errors import Error
from service.logger import Logger
from service.modelresource import ModelResource
from service.models import Model

app = Flask("app_name")
api = Api(app)

# TODO tutaj uzupelnij modele <3
simple_m = Model(SIMPLE_MODEL_NAME, "")
complex_m = Model(COMPLEX_MODEL_NAME, "")
logger = Logger(MAXIMUM_LOGS_NUMBER)

@app.errorhandler(Error)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

api.add_resource(ModelResource, "/model", "/model/user/<int:user_id>", endpoint="models", resource_class_kwargs={"simple_model": simple_m, "complex_model": complex_m, "logger": logger})

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
