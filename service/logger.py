import json
import os
from datetime import datetime
from pathlib import Path
from threading import Thread

from const import PROJECT_DIRECTORY
from service.models import Model


def save_to_file(file_name: str, logs: [], dir_name: str = "logs"):
    file_dir = os.path.join(PROJECT_DIRECTORY, dir_name)
    file_name = file_name + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    file = os.path.join(file_dir, file_name)
    Path(file_dir).mkdir(parents=True, exist_ok=True)
    with open(file, 'w') as outfile:
        json.dump({"logs": logs}, outfile)


class Logger:
    def __init__(self, save_iteration: int = 2):
        self.logs_to_save = []
        self.save_iteration = save_iteration
        self.threads_list = []

    def __del__(self):
        for thread in self.threads_list:
            thread.join()

    # TODO uzupelnic typ result
    def log(self, model: Model, data: {}, result) -> None:
        # Initialize saving if needed
        if len(self.logs_to_save) >= self.save_iteration:
            thread = Thread(target=save_to_file, args=("logs", self.logs_to_save))
            self.threads_list.append(thread)
            thread.start()
            self.logs_to_save = []
        # Clean finished threads
        self.threads_list = [thread for thread in self.threads_list if thread.is_alive()]

        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # FIXME Nie wiem czy ten message potrzebny w sumie
        entry = {"timestamp": date_time, "model": model.name, "result": result, "data": data}

        self.logs_to_save.append(entry)
