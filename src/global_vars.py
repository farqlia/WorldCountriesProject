from pathlib import Path
from os import getcwd

DATA_PATH = Path(__file__).parents[1].joinpath('data')
LOG_ERRORS_FILE = Path(__file__).parents[0].joinpath('logging_errors', 'log_errors.logs')
if LOG_ERRORS_FILE.exists():
    LOG_ERRORS_FILE.write_text("")
NUMBER_OF_COUNTRIES = 236