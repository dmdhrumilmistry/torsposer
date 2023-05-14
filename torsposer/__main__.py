from argparse import ArgumentParser
from .exposer import TorServiceExposer
from textwrap import dedent

if __name__ == '__main__':
    print(dedent('''
     dMMMMMMP .aMMMb  dMMMMb  .dMMMb  dMMMMb  .aMMMb  .dMMMb  dMMMMMP dMMMMb 
       dMP   dMP"dMP dMP.dMP dMP" VP dMP.dMP dMP"dMP dMP" VP dMP     dMP.dMP 
      dMP   dMP dMP dMMMMK"  VMMMb  dMMMMP" dMP dMP  VMMMb  dMMMP   dMMMMK"  
     dMP   dMP.aMP dMP"AMF dP .dMP dMP     dMP.aMP dP .dMP dMP     dMP"AMF   
    dMP    VMMMP" dMP dMP  VMMMP" dMP      VMMMP"  VMMMP" dMMMMMP dMP dMP    
    --------------------------------------------------------------------------
    Written By: dmdhrumilmistry
    GitHub: https://github.com/dmdhrumilmistry/torsposer
    --------------------------------------------------------------------------
    Warning: works only on debian based OSes!!
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ''').strip())
    
    parser = ArgumentParser(prog='torsposer', description='Automates procedure to expose local services to TOR network as hidden service')
    parser.add_argument('-s', '--service', dest='service_name', required=True, type=str, help='tor hidden service name')
    parser.add_argument('-sp', '--s-port', dest='service_port', required=False, type=int, default=80, help='local service port to be exposed. default: 80')
    parser.add_argument('-tp', '--t-port', dest='tor_port', required=False, type=int, default=80, help='tor host port which will be used by tor clients to connect to the tor service. default: 80')
    args = parser.parse_args()

    automate = TorServiceExposer(
        srv_name=args.service_name,
        srv_port=args.service_port,
        tor_port=args.tor_port,
    )
    automate.run()
