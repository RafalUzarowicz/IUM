import unittest
from service.modelresource import check_data
from service.errors import errors
from service.data_format import purchase_data_example


class TestDataCheck(unittest.TestCase):
    def test_example(self):
        self.assertIsNone(check_data(purchase_data_example))

    def test_type(self):
        self.assertEqual(errors["wrong_data"], check_data([]))
        self.assertEqual(errors["wrong_data"], check_data(2))
        self.assertEqual(errors["wrong_data"], check_data(None))

    def test_columns(self):
        test_example = purchase_data_example.copy()
        test_example.pop("price")

        self.assertEqual(errors["wrong_columns"], check_data(test_example))
        self.assertEqual(errors["wrong_columns"], check_data({}))
        self.assertNotEqual(errors["wrong_columns"], check_data(purchase_data_example))

    def test_purchase_timestamp(self):
        test_example_list = [purchase_data_example.copy() for _ in range(3)]
        test_example_list[0]["purchase_timestamp"] = "2021-04-01T15:52:47:12"
        test_example_list[1]["purchase_timestamp"] = ""
        test_example_list[2]["purchase_timestamp"] = "2021-04-73T15:52:47"

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_purchase_timestamp"], check_data(test_example))

    def test_delivery_company(self):
        test_example_list = [purchase_data_example.copy() for _ in range(3)]
        test_example_list[0]["delivery_company"] = "tak"
        test_example_list[1]["delivery_company"] = ""
        test_example_list[2]["delivery_company"] = "2.0"

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_delivery_company"], check_data(test_example))

    def test_product_id(self):
        test_example_list = [purchase_data_example.copy() for _ in range(3)]
        test_example_list[0]["product_id"] = "tak"
        test_example_list[1]["product_id"] = ""
        test_example_list[2]["product_id"] = "2.0"

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_product_id"], check_data(test_example))

    def test_offered_discount(self):
        test_example_list = [purchase_data_example.copy() for _ in range(3)]
        test_example_list[0]["offered_discount"] = "tak"
        test_example_list[1]["offered_discount"] = ""
        test_example_list[2]["offered_discount"] = "2.0"

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_offered_discount"], check_data(test_example))

    def test_price(self):
        test_example_list = [purchase_data_example.copy() for _ in range(2)]
        test_example_list[0]["price"] = "tak"
        test_example_list[1]["price"] = ""

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_price"], check_data(test_example))

    def test_street(self):
        test_example_list = [purchase_data_example.copy() for _ in range(3)]
        test_example_list[0]["street"] = "tak"
        test_example_list[1]["street"] = "ulica ulica"
        test_example_list[2]["street"] = "ulica 23"
        test_example_list[2]["street"] = ""

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_street"], check_data(test_example))

    def test_street_number(self):
        test_example_list = [purchase_data_example.copy() for _ in range(3)]
        test_example_list[0]["street"] = "pl. Brzoskwiniowa 11-2"
        test_example_list[1]["street"] = "pl. Brzoskwiniowa 11.53"
        test_example_list[2]["street"] = "pl. Brzoskwiniowa 11+53"
        test_example_list[2]["street"] = "pl. Brzoskwiniowa 11/5."

        for test_example in test_example_list:
            self.assertEqual(errors["wrong_street_number"], check_data(test_example))