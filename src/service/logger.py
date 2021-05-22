from datetime import datetime
from threading import Thread

from src.service.models import Model

# TODO saving
def save_to_file(file_name: str, logs: [], file_path: str = "./"):
    print("THREAD XD")


class Logger:
    def __init__(self, save_iteration: int = 2):
        self.logs_to_save = []
        self.save_iteration = save_iteration
        self.threads_list = []

    def __del__(self):
        for thread in self.threads_list:
            thread.join()

    # TODO uzupelnic typ result
    def log(self, message: str, model: Model, data: {}, result) -> None:
        if len(self.logs_to_save) >= self.save_iteration:
            thread = Thread(target=save_to_file, args=("", self.logs_to_save))
            self.threads_list.append(thread)
            thread.start()
            self.logs_to_save = []

        date_time = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

        entry = {"message": message, "timestamp": date_time, "model": model.name, "result": result, "data": data}

        self.logs_to_save.append(entry)

        print("LOG:", date_time, " ", message, " ", model.name, " ", result, " ", data)
