import logging
from logging import FileHandler
import os

format_file = '[%(asctime)s][pid:%(process)d][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s'


def get_logger(file_path, level=logging.DEBUG):
    log_name = file_path.split('/')[-1]
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    file_handler = FileHandler(filename=file_path, mode='w')
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(format_file))
    logger.addHandler(file_handler)
    return logger


def get_path(parent, file_path):
    # if '/' in file_path:
    #     name = file_path.split('/')[-1]
    #     index = file_path.index(name)
    #     log_dir = parent + file_path[0: index]
    # else:
    #     name = file_path
    #     log_dir = parent
    path = os.path.join(parent, file_path)
    log_dir = os.path.dirname(path)
    print(f"log_dir:{log_dir}")
    if not os.path.exists(log_dir):
        os.mkdir(f'{log_dir}')
    return path
