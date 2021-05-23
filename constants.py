import os

PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

HOST = "127.0.0.1"
PORT = 5000


DEFAULT_LOGS_NUMBER = 10
DEFAULT_LOG_DIR_NAME = "logs"
DEFAULT_LOG_FILES_PREFIX = "log"
LOG_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

SIMPLE_MODEL_NAME = "simple"
COMPLEX_MODEL_NAME = "complex"