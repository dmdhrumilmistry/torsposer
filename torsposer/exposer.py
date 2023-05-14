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


    def install_requirements(self):
        '''Install required debian packages

        Arguments:
            None

        Returns:
            str: returns executed installation output
        '''
        # check if tor exists
        try:
            output, _ = run_cmd('tor --version')
            tor_version:str = output.splitlines()[0].split(' ')[2]
            output = f'TOR found with version {tor_version}'
            logger.info(output)
            output
        except FileNotFoundError:
            logger.error('TOR is not installed')

            logger.info('Installing TOR package')
            output, code = run_cmd('sudo apt install tor -y')
            if code == 0:
                logger.info('Tor package installed successfully')
            else:
                logger.error('Tor package installation failed')

        return output


    def create_torrc_file_content(self):
        '''Creates torrc file according to specified configuration in constructor
        
        Arguments:
            None

        Returns:
            str: returns tor file content according to specified configuration
        '''
        # read torrc file
        torrc_content = read_file(self.__torrc_path)
        
        # take backup of torrc file
        bak_file = path_join(getcwd(), f'before-{self._srv_name}-torrc.bak')
        write_file(bak_file, torrc_content)
        logger.info(f'succesfully backed up torrc file at {bak_file}')

        # check if tor file is default tor conf then replace complete conf
        torrc_content = torrc_content.splitlines()

        if torrc_content[0] == '## Configuration file for a typical Tor user':
            torrc_file_content = dedent(f'''
            ## Enable TOR SOCKS proxy
            SOCKSPort 127.0.0.1:9050

            ## {self._srv_name} Hidden Service
            HiddenServiceDir /var/lib/tor/{self._srv_name}
            HiddenServicePort {self._tor_port} 127.0.0.1:{self._srv_port}
            ''').strip()
        else:
            # BUG: can add same service twice
            # TODO: implement mechanism to check if service is already present 
            # and avoid adding that service

            torrc_content.append(dedent(f'''
            ## {self._srv_name} Hidden Service
            HiddenServiceDir /var/lib/tor/{self._srv_name}
            HiddenServicePort {self._tor_port} 127.0.0.1:{self._srv_port}\n
            ''').strip())

            torrc_file_content = '\n'.join(torrc_content)


        return torrc_file_content
    

    def write_torrc_file(self, torrc_conf:str) -> bool:
        '''Writes data to default torrc file
        
        Arguments:
            torrc_conf (str): torrc configuration data

        Returns:
            bool: True is process is successful else False
        '''
        new_torrc_path = path_join(getcwd(), f'{self._srv_name}-torrc')
        write_file(new_torrc_path, torrc_conf)
        logger.info(f'Stored New torrc configuration stored at {new_torrc_path}')
        
        output, code = run_cmd(f'sudo cp {new_torrc_path} {self.__torrc_path}')
        logger.debug(f'Output while replacing torrc file:\n{output}')

        return True if code == 0 else False 
    

    def restart_tor_service(self):
        '''Restarts tor service
        
        Arguments:
            None

        Returns:
            None
        '''
        _, code = run_cmd('sudo service tor restart')
        if code == 0:
            logger.info('TOR service restarted successfully')
        else:
            logger.error('Failed to restart TOR service')


    def run(self):
        '''starts service automatic configuration, 
        returns True if service is configured 
        successfully else returns False
        
        Arguments:
            None

        Returns:
            bool: returns True if service is configured successfully else returns False
        '''
        self.install_requirements()

        torrc_conf = self.create_torrc_file_content()
        if self.write_torrc_file(torrc_conf):
            logger.info('torrc updated successfully')
            status = True
        else:
            logger.error('torrc updation failed. Check debug logs for more info')
            status = False

        self.restart_tor_service()

        return status
