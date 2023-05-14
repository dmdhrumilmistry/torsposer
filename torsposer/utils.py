from os import geteuid
from os.path import isfile
from subprocess import run, PIPE
from shlex import split


def run_cmd(cmd:str) -> tuple:
    '''Run shell commands
    
    Arguments:
        cmd (string): command to be executed

    Returns:
        tuple: returns executed command output/error along with status code
    '''
    result = run(split(cmd), stderr=PIPE, stdout=PIPE)
    return (result.stdout.decode('utf-8') or result.stderr.decode('utf-8'), result.returncode)


def has_sudo_perms():
    '''Checks whether user has sudo permissions or not. 
    Returns True if user has sudo permissions else False.
    
    Arguments:
        None

    Returns:
        bool: returns True if user has sudo perms else returns False
    '''
    # check user id
    if geteuid() == 0:
        return True
    
    output, status_code = run_cmd('sudo whoami')
    if output == 'root\n' and status_code == 0:
        return True
    
    return False


def read_file(path:str):
    '''returns file content if file present else returns None
    
    Arguments:
        path (str): path file

    Returns:
        str: file content if file present
        None: if file doesn't exists
    '''
    if not isfile(path):
        return

    with open(path, 'r') as f:
        content = f.read()

    return content


def write_file(path:str, content:str):
    '''overwrites file data with provided content
    
    Arguments:
        path (str): path file
        content (str): content to written into the file

    Returns:
        None
    '''
    if not isinstance(content, str):
        content = str(content)

    with open(path, 'w') as f:
        content = f.write(content)
