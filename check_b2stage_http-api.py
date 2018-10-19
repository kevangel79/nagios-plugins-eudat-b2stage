#!/usr/bin/python

import sys, requests
import argparse

# ##############################################################################
# B2STAGE Client  #
# ##############################################################################


def ValidateValues(arguments):
        """ Validate values - input values """

        if arguments.timeout <= 0:
            print("\nInvalid timeout value: %s\n" % arguments.timeout)
            print_help()
            exit()

        if arguments.hostname is None:
            print("\nNo hostname provided\n")
            print_help()
            exit()

        if not arguments.hostname.startswith("http"):
            print("\nNo schema supplied with hostname, did you mean https://%s?\n" % arguments.hostname)
            print_help()
            exit()

def print_help():
        """ Print help values."""

        print "usage: check_b2stage_http-api.py -H -p"
        print "--- ---- ---- ---- ---- ---- ----\n"
        print "main arguments:"
        print "-H hostname"
        print "\n"
        print "optional arguments:"
        print " -h, --help  show this help message and exit"
        print "-p port"
        print "-t timeout"
        print "-v verbose"



def debugValues(arguments):
    """ Print debug values.
        Args:
            arguments: the input arguments
    """
    if arguments.debug:
        print "[debugValues] - hostname:"+ arguments.hostname
    if arguments.port!='':
        print "[debugValues] - port:" + arguments.port
    if arguments.timeout!='':
        print "[debugValues] - timeout:" + str(arguments.timeout)
    if arguments.t!='':
        print "[debugValues] - timeout:" + str(arguments.t)

def checkHealth(URL,timeout):
    """ Check service status.
        Args:
           URL : service hostname
           timeout : how long should we wati 
    """
    try:
        out = requests.get(url=URL, timeout=timeout)

        content = out.json()

        if out.status_code != 200:
            description = "WARNING - Unexpected status code %s" % out.status_code
            exit_code = 1

        if content['Response']['data'] != "Server is alive!":
            description = "WARNING - Unexpected response: %s" % content['Response']['data']
            exit_code = 1

        description = "OK - Service reachable"
        exit_code = 0

    except requests.exceptions.ConnectionError:
        description = "CRITICAL - Service unreachable"
        exit_code = 2

    description = "UNKNOWN - Status unknown"
    exit_code = 3
    return description, exit_code

def printResult(description, exit_code):
    """ Print the predefined values 
        Args:
            description: the nagios description
            exit_code: the code that should be returned to nagios
    """

    print 'description'
    sys.exit(exit_code)

def main():

    parser = argparse.ArgumentParser(description='B2STAGE probe '
                                                 'Supports healthcheck.')
    parser.add_argument("--hostname", "-H", help='The Hostname of B2STAGE service')
    parser.add_argument("--port", "-p", type=int)
    parser.add_argument("--timeout", "-t", metavar="seconds", help="Timeout in seconds. Must be greater than zero", type=int, default=30)
    parser.add_argument("--verbose","-v", dest='debug', help='Set verbosity level', action='count', default=0)
    arguments = parser.parse_args()
    ValidateValues(arguments)
    NAGIOS_RESULT = 0

    URL=arguments.hostname
    if arguments.port is not None:
       URL += ":%s" % arguments.port

    URL += "/api/status"
    timeout = arguments.timeout
    description, exit_code = checkHealth(URL,timeout)
    printResult(description, exit_code)


if __name__ == "__main__":
    main()

