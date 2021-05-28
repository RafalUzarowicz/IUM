import unittest

from service.errors import Error, errors
from service.logger import Logger
from service.modelresource import ModelResource, TestModelResource, LoggerResource
from service.application import app, complex_m, simple_m
from service.data_format import purchase_data_example

from constants import PORT


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.baseURL = "http://127.0.0.1:" + str(PORT) + "/model"
        self.payload = purchase_data_example

    def test_get(self):
        rv = self.client.get("/model", json=self.payload)
        self.assertEqual(200, rv.status_code)

    def test_get_wrong_url(self):
        rvs_params = [
            {"url": "/model/user/", "param": "abc", "payload": purchase_data_example.copy()},
            {"url": "/models/", "param": "-12", "payload": purchase_data_example.copy()},
            {"url": "/model/user/", "param": "", "payload": purchase_data_example.copy()},
        ]

        for rv_params in rvs_params:
            rv = self.client.get(rv_params["url"] + rv_params["param"], json=rv_params["payload"])
            self.assertEqual(404, rv.status_code)

    def test_get_wrong_model_name(self):
        model_names = [
            "abc",
            -12,
            "test"
        ]
        model_res = ModelResource(complex_m, simple_m, Logger(100))
        for model_name in model_names:
            with self.assertRaises(Error) as ec:
                model_res.get(model_name)
            e = ec.exception
            self.assertEqual(errors["wrong_model_name"]["message"], e.message)
            self.assertEqual(errors["wrong_model_name"]["code"], e.status_code)

    def test_get_wrong_data_type(self):
        rv = self.client.get("/model", data=self.payload)
        self.assertEqual(errors["wrong_data_type"]["message"], rv.get_json()["message"])
        self.assertEqual(415, rv.status_code)

    def test_get_wrong_columns(self):
        temp_data = purchase_data_example.copy()
        temp_data.pop("street")
        rv = self.client.get("/model", json=temp_data)
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
            rv = self.client.get("/model", json=payload)
            self.assertEqual(errors[changes[i][2]]["message"], rv.get_json()["message"])
            self.assertEqual(errors[changes[i][2]]["code"], rv.status_code)


class ExperimentAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.baseURL = "http://127.0.0.1:" + str(PORT) + "/model"
        self.payload = purchase_data_example

    def test_get(self):
        rv = self.client.get("/test/user/12", json=self.payload)
        self.assertEqual(200, rv.status_code)

    def test_get_wrong_url(self):
        rvs_params = [
            {"url": "/model/user/", "param": "abc", "payload": purchase_data_example.copy()},
            {"url": "/models/", "param": "-12", "payload": purchase_data_example.copy()},
            {"url": "/model/user/", "param": "", "payload": purchase_data_example.copy()},
        ]

        for rv_params in rvs_params:
            rv = self.client.get(rv_params["url"] + rv_params["param"], json=rv_params["payload"])
            self.assertEqual(404, rv.status_code)

    def test_get_wrong_user_id(self):
        user_ids = [
            "abc",
            -12,
            {}
        ]
        model_res = TestModelResource(complex_m, simple_m, Logger(100))
        for user_id in user_ids:
            with self.assertRaises(Error) as ec:
                model_res.get(user_id)
            e = ec.exception
            self.assertEqual(errors["wrong_user_id"]["message"], e.message)
            self.assertEqual(errors["wrong_user_id"]["code"], e.status_code)

    def test_get_wrong_data_type(self):
        rv = self.client.get("/test/user/12", data=self.payload)
        self.assertEqual(errors["wrong_data_type"]["message"], rv.get_json()["message"])
        self.assertEqual(415, rv.status_code)

    def test_get_wrong_columns(self):
        temp_data = purchase_data_example.copy()
        temp_data.pop("street")
        rv = self.client.get("/test/user/12", json=temp_data)
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
            rv = self.client.get("/test/user/12", json=payload)
            self.assertEqual(errors[changes[i][2]]["message"], rv.get_json()["message"])
            self.assertEqual(errors[changes[i][2]]["code"], rv.status_code)


class LoggerTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.baseURL = "http://127.0.0.1:" + str(PORT) + "/test"

    def test_put(self):
        rv = self.client.put("/log/10")
        self.assertEqual(200, rv.status_code)

    def test_put_wrong_url(self):
        rvs_params = [
            {"url": "/model/user/", "param": "abc"},
            {"url": "/xd/", "param": "-12"},
            {"url": "/model/user/", "param": ""},
        ]

        for rv_params in rvs_params:
            rv = self.client.put(rv_params["url"] + rv_params["param"])
            self.assertEqual(404, rv.status_code)

    def test_put_wrong_log_num(self):
        logs_nums = [
            "abc",
            -12,
            {}
        ]
        res = LoggerResource(Logger())
        for log_num in logs_nums:
            with self.assertRaises(Error) as ec:
                res.put(log_num)
            e = ec.exception
            self.assertEqual(errors["wrong_log_num"]["message"], e.message)
            self.assertEqual(errors["wrong_log_num"]["code"], e.status_code)

    def test_put_good_log_num(self):
        logs_nums = [
            10,
            100,
            50
        ]
        logger = Logger()
        res = LoggerResource(logger)
        for log_num in logs_nums:
            res.put(log_num)
            self.assertEqual(log_num, logger.save_iteration)
