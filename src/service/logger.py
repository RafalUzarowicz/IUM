# TODO logs
from datetime import datetime

from src.service.models import Model


class Logger:
    def __init__(self):
        self.logs_counter = 0
        self.logs_to_save = []
    # TODO uzupelnic typ result
    def log(self, message: str, model: Model, data: {}, result) -> None:
        self.logs_counter = self.logs_counter + 1

        date_time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

        entry = {"message": message, "timestamp": date_time, "model": model.name, "result": result, "data": data}
        self.logs_to_save.append(entry)
        print(date_time, " ", message, " ", model.name, " ", result, " ", data)