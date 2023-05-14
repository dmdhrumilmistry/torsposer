from textwrap import dedent
from os import getcwd
from os.path import join as path_join, isfile
from .utils import run_cmd, has_sudo_perms, read_file, write_file


import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

class SudoPermsAbsentException(Exception):
    '''Exception to be raised if user doesn't have sudo permissions'''
    pass


class TorServiceExposer:
    '''Class to create tor hidden service'''
    def __init__(self, srv_name:str='torsposer', srv_port:int=8000, tor_port:int=80) -> None:
        '''TorServiceExposer class constructor.
        
        Arguments:
            srv_name (str): name of the hidden service
            srv_port (int): port on which hidden service will be running
            tor_port (int): port on which tor should expose hidden service

        Returns:
            None
        '''
        self._srv_name = srv_name.lower().replace(' ', '_')
        self._srv_port = srv_port
        self._tor_port = tor_port

        self.__torrc_path = '/etc/tor/torrc'

        if not has_sudo_perms():
            raise SudoPermsAbsentException("Run again after running `$ sudo whoami` command in terminal to get sudo perms or run with root user")


    def create_torrc_file(self):
        '''Creates torrc file according to specified configuration in constructor
        
        Arguments:
            None

        Returns:
            boolean: True if successfull else False
        '''
        # read torrc file
        torrc_content = read_file(self.__torrc_path)
        
        # take backup of torrc file
        bak_file = path_join(getcwd(), f'{self._srv_name}-torrc.bak')
        write_file(bak_file, torrc_content)
        logger.info(f'succesfully backed up torrc file at {bak_file}')

        # create torrc configuration
        torrc_file_content = dedent(f'''
        ## Enable TOR SOCKS proxy
        SOCKSPort 127.0.0.1:9050

        ## {self._srv_name} Hidden Service
        HiddenServiceDir /var/lib/tor/{self._srv_name}
        HiddenServicePort {self._tor_port} 127.0.0.1:{self._srv_port}
        ''').strip()
        
        return torrc_file_content


if __name__ == '__main__':
    res = TorServiceExposer().create_torrc_file()

    print(res)