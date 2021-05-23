import unittest

from service.errors import Error, errors
from service.logger import Logger
from service.modelresource import ModelResource
from service.application import app, complex_m, simple_m
from service.data_format import purchase_data_example

from constants import HOST, PORT


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.baseURL = "http://" + HOST + ":" + str(PORT) + "/model"
        self.payload = purchase_data_example

    def test_get(self):
        rv = self.client.get("/model/user/12", json=self.payload)
        self.assertEqual(200, rv.status_code)

    def test_get_wrong_url(self):
        rvs_params = [
            {"url": "/model/user/", "user_id": "abc", "payload": purchase_data_example.copy()},
            {"url": "/model/user/", "user_id": "-12", "payload": purchase_data_example.copy()},
            {"url": "/model/user/", "user_id": "", "payload": purchase_data_example.copy()},
        ]

        for rv_params in rvs_params:
            rv = self.client.get(rv_params["url"] + rv_params["user_id"], json=rv_params["payload"])
            self.assertEqual(404, rv.status_code)

    def test_get_wrong_user_id(self):
        user_ids = [
            "abc",
            -12,
            {}
        ]
        model_res = ModelResource(complex_m, simple_m, Logger(100))
        for user_id in user_ids:
            with self.assertRaises(Error) as ec:
                model_res.get(user_id)
            e = ec.exception
            self.assertEqual(errors["wrong_user_id"]["message"], e.message)
            self.assertEqual(errors["wrong_user_id"]["code"], e.status_code)

    def test_get_wrong_data_type(self):
        rv = self.client.get("/model/user/12", data=self.payload)
        self.assertEqual(errors["wrong_data_type"]["message"], rv.get_json()["message"])
        self.assertEqual(415, rv.status_code)

    def test_get_wrong_columns(self):
        temp_data = purchase_data_example.copy()
        temp_data.pop("street")
        rv = self.client.get("/model/user/12", json=temp_data)
        self.assertEqual(errors["wrong_columns"]["message"], rv.get_json()["message"])
        self.assertEqual(422, rv.status_code)

    def test_get_wrong_data(self):
        changes = [
            ("purchase_timestamp", "2021-04-01T15:52:47:242515", "wrong_purchase_timestamp"),
            ("delivery_company", "UPS", "wrong_delivery_company"),
            ("product_id", "tak", "wrong_product_id"),
            ("price", -14, "wrong_price"),
            ("offered_discount", "nie", "wrong_offered_discount"),
            ("street", "pl. Brzoskwiniowa", "wrong_street"),
            ("street", "pl. Brzoskwiniowa 11.53", "wrong_street_number")
        ]
        payloads = []

        for change in changes:
            temp_data = purchase_data_example.copy()
            temp_data[change[0]] = change[1]
            payloads.append(temp_data)

        for i, payload in enumerate(payloads):
            rv = self.client.get("/model/user/12", json=payload)
            self.assertEqual(errors[changes[i][2]]["message"], rv.get_json()["message"])
            self.assertEqual(errors[changes[i][2]]["code"], rv.status_code)
