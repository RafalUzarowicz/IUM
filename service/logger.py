import json
import os
from datetime import datetime
from pathlib import Path
from threading import Thread

from constants import PROJECT_DIRECTORY
from service.models import Model


def save_to_file(file_name: str, logs: [], dir_name: str = "logs") -> None:
    file_dir = os.path.join(PROJECT_DIRECTORY, dir_name)
    file_name = file_name + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jsonl"
    file = os.path.join(file_dir, file_name)
    Path(file_dir).mkdir(parents=True, exist_ok=True)
    with open(file, 'a') as outfile:
        for i, log in enumerate(logs):
            json.dump(log, outfile)
            if i < len(logs) - 1:
                outfile.write("\n")



class Logger:
    def __init__(self, save_iteration: int = 10):
        self.logs_to_save = []
        self.save_iteration = save_iteration
        self.threads_list = []

    def __del__(self):
        for thread in self.threads_list:
            thread.join()

    # TODO tutaj uzupelnic typ result
    def log(self, model: Model, data: {}, result) -> None:
        # Initialize saving if needed
        if len(self.logs_to_save) >= self.save_iteration:
            thread = Thread(target=save_to_file, args=("log", self.logs_to_save))
            self.threads_list.append(thread)
            thread.start()
            self.logs_to_save = []
        # Clean finished threads
        self.threads_list = [thread for thread in self.threads_list if thread.is_alive()]

        # Log
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        entry = {"timestamp": date_time, "model": model.name, "result": result, "data": data}
        self.logs_to_save.append(entry)
