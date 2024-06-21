from command import cmd
import os
import json
import threading
import logging
from tqdm import tqdm

logging.basicConfig(filename='k8s-install.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def log():
    return logging


LOG = log()

stdlib_dir = '{0}/k8s-install.log'.format(os.path.dirname(__file__))
print('LOG FILE : ', stdlib_dir)


def execute_job(thread, name, parameters, pbar):
    LOG.info(f'{thread} - {name}')
    for command in parameters:
        message = command['message']
        comman_exec = command['command']
        parameters = command['parameters']
        comman_exec = comman_exec.format(**parameters)
        output = cmd.execute_command(thread, comman_exec, message)   
        pbar.update(1)

def main():
    # COMMAND IN JSON
    file = os.path.join(os.getcwd(), 'command/command.json')
    # OPEN JSON
    with open(file, 'r') as archivo:
        # LOAD JSON
        data = json.load(archivo)
    total_commands = sum(len(job['commands']) for item in data for job in item['stage']['threads'])
    # PROGRESS BAR
    with tqdm(total=total_commands, ncols=100, desc="Create Clust k8s: master + nodes") as pbar:
        for item in data:
            i = 0
            name = item['stage']['name']
            jobs = item['stage']['threads']
            threads = []
            for job in jobs:
                i = i + 1
                commands = job['commands']
                thread = threading.Thread(target=execute_job, args=(f'thread-{i}', name, commands, pbar))
                threads.append(thread)
                thread.start()
            # WAITING JOBS ALLS
            for thread in threads:
                thread.join()            

if __name__ == "__main__":
    main()