import subprocess
import logging
import os
import random, string

logging.basicConfig(filename='k8s-install.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def log():
    return logging
LOG = log()

# EXECUTE COMMAND
def execute_command(thread:str=None, command:str=None, message:str=None):
    if command:
        if message:
            LOG.info(f'{thread} - message: {message}')
        LOG.info(f'{thread} - command: {command}')

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = ''
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output = output.strip()
                LOG.info(f'{thread} - output: {output}')                
        return output