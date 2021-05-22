from flask import Flask
from flask_restful import Api

from src.service.logger import Logger
from src.service.modelresource import ModelResource
from src.service.models import Model

app = Flask("app_name")
api = Api(app)

# TODO tutaj uzupelnij modele <3
simple_m = Model("simple", "")
complex_m = Model("complex", "")
logger = Logger()

api.add_resource(ModelResource, "/model", "/model/userid/<int:user_id>", endpoint="models", resource_class_kwargs={"simple_model": simple_m, "complex_model": complex_m, "logger": logger})

if __name__ == "__main__":
    app.run(debug=True)
