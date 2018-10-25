#!/usr/bin/python

import sys
import requests
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

        print("usage: check_b2stage_http-api.py -H -p")
        print("--- ---- ---- ---- ---- ---- ----\n")
        print("main arguments:")
        print("-H hostname")
        print("\n")
        print("optional arguments:")
        print(" -h, --help  show this help message and exit")
        print("-p port")
        print("-t timeout")
        print("-v verbose")


def debugValues(arguments):
    """ Print debug values.
        Args:
            arguments: the input arguments
    """
    if arguments.debug:
        print("[debugValues] - hostname: %s" % arguments.hostname)
    if arguments.port != '':
        print("[debugValues] - port: %s" % arguments.port)
    if arguments.timeout != '':
        print("[debugValues] - timeout: %s" % arguments.timeout)
    if arguments.t != '':
        print("[debugValues] - timeout: %s" % arguments.t)


def checkHealth(URL, timeout):
    """ Check service status.
        Args:
           URL : service hostname
           timeout : how long should we wati
    """
    try:
        out = requests.get(url=URL, timeout=timeout)

        if out.status_code != 200:
            description = "WARNING - Unexpected status code %s" % out.status_code
            exit_code = 1
            return description, exit_code

        content = out.json()
        resp = content['Response']['data']

        if resp != "Server is alive!":
            description = "WARNING - Unexpected response: %s" % resp
            exit_code = 1
            return description, exit_code

        description = "OK - Service reachable"
        exit_code = 0
        return description, exit_code

    except requests.exceptions.ConnectionError:
        description = "CRITICAL - Service unreachable"
        exit_code = 2
        return description, exit_code

    description = "UNKNOWN - Status unknown"
    exit_code = 3
    return description, exit_code


def printResult(description, exit_code):
    """ Print the predefined values
        Args:
            description: the nagios description
            exit_code: the code that should be returned to nagios
    """

    print(description)
    sys.exit(exit_code)


def main():

    parser = argparse.ArgumentParser(description='B2STAGE probe '
                                                 'Supports healthcheck.')
    parser.add_argument("--hostname", "-H", help='The Hostname of B2STAGE service')
    parser.add_argument("--port", "-p", type=int)
    parser.add_argument("--timeout", "-t", metavar="seconds", help="Timeout in seconds. Must be greater than zero", type=int, default=30)
    parser.add_argument("--verbose", "-v", dest='debug', help='Set verbosity level', action='count', default=0)
    arguments = parser.parse_args()
    ValidateValues(arguments)
    NAGIOS_RESULT = 0

    URL = arguments.hostname
    if arguments.port is not None:
        URL += ":%s" % arguments.port

    URL += "/api/status"
    timeout = arguments.timeout
    description, exit_code = checkHealth(URL, timeout)
    printResult(description, exit_code)


if __name__ == "__main__":
    main()
