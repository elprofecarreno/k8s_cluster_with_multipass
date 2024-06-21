import subprocess
import logging
import os
import random, string

logging.basicConfig(filename='k8s-install.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def log():
    return logging


LOG = log()


def random_name(size=16):
    characters = string.ascii_letters + string.digits
    name = ''.join(random.choice(characters) for _ in range(size))
    return name

def create_file(file):
    with open(file, 'w') as f:
        f.write('')

def read_file(file):
    with open(f'{file}', 'r') as f:
            content = f.read()            
    output = content.replace('\n', '')                
    return output

def delete_file(file):
    if os.path.exists(file):
        os.remove(file)

# EXECUTE COMMAND
def execute_command(thread:str=None, command:str=None, message:str=None):
    file_name = random_name() + '.txt'
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