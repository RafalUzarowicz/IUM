# TODO remove this random
import random


class Model:
    def __init__(self, name: str, plk_file_path: str):
        self.name = name
        # TODO tutaj modele

    def predict(self, data) -> int:
        # TODO ma zwracac inta? floata? minuty? godziny? jak zyc?
        return random.randint(0, 100)
