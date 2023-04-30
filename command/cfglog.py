import logging

logging.basicConfig(filename='k8s-install.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def log():
    return logging