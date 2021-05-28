import pickle
import os

import pandas as pd

from service.preprocessing import apply


class Model:
    ENCODER_FILEPATH = os.path.dirname(__file__) + "\\" + os.path.relpath("pretrained/oh_encoder.pkl")

    def __init__(self, name: str, plk_file_path: str):
        self.name = name
        plk_file_path = os.path.dirname(__file__) + "\\" + os.path.relpath(plk_file_path)
        with open(plk_file_path, "rb") as f:
            self.model = pickle.load(f)
        with open(self.ENCODER_FILEPATH, "rb") as enc:
            self.encoder = pickle.load(enc)

    def predict(self, data: {}) -> int:
        df = pd.DataFrame({k: [v] for k, v in data.items()})
        df = apply(df)
        categoricals = df.select_dtypes(object).columns.to_list()
        categoricals.append("delivery_company")
        encoded = pd.DataFrame(self.encoder.transform(df[categoricals]), index=df.index)
        df = pd.concat([df.drop(categoricals, axis=1), encoded], axis=1)
        res = self.model.predict(df)
        return int(round(res[0]))
