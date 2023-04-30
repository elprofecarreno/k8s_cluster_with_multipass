import subprocess

# EXECUTE OS COMMAND
def exec_command(commands):
    return subprocess.run(commands, shell=True, capture_output=True, text=True, encoding="utf-8").stdout