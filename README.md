
# B2STAGE plugin for Nagios

Nagios plugin to check B2STAGE functionality

## Usage

### NAME

```
      check_b2stage_http-api.py - B2STAGE Http API Nagios plugin
```

### DESCRIPTION

	RESTful HTTP-API for the B2STAGE service inside the EUDAT project.
	The plugin checks the health of B2STAGE HTTP-API service.

### SYNOPSIS

```
      check_b2stage_http-api.py [--version] [--help] [--verbose <level>]
                   [--timeout <threshold> ] --hostname <host> [--port <port>]
```

      Options:
       --help,-h         : Display this help.
       --verbose,-v      : Same as debug option (0-9).
       --timeout,-t      : Time threshold to wait before timeout (in second).

       --hostname,-H     : The B2STAGER server host <name or IP).
       --port         : The B2STAGE server port.

### OPTIONS

    --version
         Display plugins version.
    --help
         Display this help.

    --verbose 
         Same as debug option.

    --timeout
         Time threshold in second to wait before timeout (default to 30).

    --hostname <host>
         The B2STAGE server host. It can be a DNS name or an IP address.

    --port <port>
         The B2STAGE server port (default to 80).


### EXAMPLES
      Using  script:

```
   ./check_b2stage_http-api.py -H www.b2stage.fr -p 443
```

