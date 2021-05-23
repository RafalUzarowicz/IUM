columns = [
    {"name": "purchase_timestamp"},
    {"name": "delivery_company"},
    {"name": "product_id"},
    {"name": "product_name", "pattern": r".*"},
    {"name": "category_path", "pattern": r".*"},
    {"name": "price"},
    {"name": "offered_discount"},
    {"name": "city", "pattern": r".*"},
    {"name": "street", "pattern": r".*"}
]
# FIXME to tak sobie dla przykladu zrobilem pewnie do usuniecia albo jak sie uzupelni valid rzeczami to do testow
purchase_data_example = {
    "purchase_timestamp": "2021-04-01T15:52:47",
    "delivery_company": 620,
    "product_id": 1001,
    "product_name": "Telefon Siemens Gigaset DA310",
    "category_path": "Telefony i akcesoria;Telefony stacjonarne",
    "price": 58.97,
    "offered_discount": 5,
    "city": "Police",
    "street": "pl. Brzoskwiniowa 11/53"
}
