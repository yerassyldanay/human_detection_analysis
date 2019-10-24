import logging

logging.basicConfig(filename='./utils/log/app.log', level=logging.INFO, format='%(asctime)s %(name)s: %(levelname)s %(message)s')

def get_logger(name: str):
    return logging.getLogger(name)
