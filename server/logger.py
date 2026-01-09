from datetime import datetime
import os
import json


def build_log(level: str, message: str, data: dict):

    log = {
        "time": str(datetime.now()),
        "level": level,
        "message": message,
    }

    if data is not None:
        log["data"] = data

    return log


def write_log(filename: str, log: dict):
    with open(filename, "a") as file:
        file.write(json.dumps(log) + "\n")


def log_info(message: str, data: dict = None):
    log = build_log("INFO", message, data)
    write_log("logs/info.log", log)


def log_error(message: str, data: dict = None):
    log = build_log("ERROR", message, data)
    write_log("logs/error.log", log)
