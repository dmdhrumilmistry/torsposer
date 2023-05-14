# TOR Service Exposer (torsposer)

```
dMMMMMMP .aMMMb  dMMMMb  .dMMMb  dMMMMb  .aMMMb  .dMMMb  dMMMMMP dMMMMb 
   dMP   dMP"dMP dMP.dMP dMP" VP dMP.dMP dMP"dMP dMP" VP dMP     dMP.dMP 
  dMP   dMP dMP dMMMMK"  VMMMb  dMMMMP" dMP dMP  VMMMb  dMMMP   dMMMMK"  
 dMP   dMP.aMP dMP"AMF dP .dMP dMP     dMP.aMP dP .dMP dMP     dMP"AMF   
dMP    VMMMP" dMP dMP  VMMMP" dMP      VMMMP"  VMMMP" dMMMMMP dMP dMP
```

Expose Services to the TOR network automatically


## Installation

### Using PyPi

- Use pip 

    ```bash
    python3 -m pip install torsposer
    ```

### Using GitHub + Pip

- Install requirements
    - Git

- Use below command

    ```bash
    python3 -m pip install git+https://github.com/dmdhrumilmistry/torsposer.git
    ```

## Usage

- Help menu

    ```bash
    ❯ torsposer
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
    usage: torsposer [-h] -s SERVICE_NAME [-sp SERVICE_PORT] [-tp TOR_PORT]
    torsposer: error: the following arguments are required: -s/--service
    ```

- expose localhost server running on port 80 to tor network on tor host port 80

    ```bash
    torsposer -s http_service -sp 80 -tp 80
    ```

> Note: if `torsposer` doesn't work try replacing it with `python3 -m torsposer`
