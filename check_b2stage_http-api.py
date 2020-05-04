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
        print("-u user")
        print("-P password")


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
    if arguments.user != '':
        print("[debugValues] - user: %s" % arguments.user)
    if arguments.password != '':
        print("[debugValues] - password: ******")


def checkHealth(URL, timeout):
    """ Check service status.
        Args:
           URL : service hostname
           timeout : how long should we wait for a response from the server
    """
    out = None
    u = URL + "/api/status"
    try:
        out = requests.get(url=u, timeout=timeout)

    except requests.exceptions.SSLError:
        description = "WARNING - Invalid SSL certificate"
        exit_code = 1
        return description, exit_code
    except requests.exceptions.ConnectionError:
        description = "CRITICAL - Service unreachable"
        exit_code = 2
        return description, exit_code

    if out is None:
        description = "UNKNOWN - Status unknown"
        exit_code = 3
        return description, exit_code

    if out.status_code != 200:
        description = "WARNING - Unexpected status code %s" % out.status_code
        exit_code = 1
        return description, exit_code

    content = out.json()
    if 'Response' in content:
        resp = content['Response']['data']
    else:
        resp = content

    if not resp.startswith("Server is alive"):
        description = "WARNING - Unexpected response: %s" % resp
        exit_code = 1
        return description, exit_code

    description = "OK - Service reachable"
    exit_code = 0
    return description, exit_code


def checkAuthentication(URL, timeout, user, password):
    """ Check service authentication.
        Args:
           URL : service hostname
           timeout : how long should we wait for a response from the server
           user : username to authenticate the session
           password : password to authenticate the session
    """

    token = None
    out = None
    u = URL + "/auth/b2safeproxy"
    try:
        payload = {'username': user, 'password': password}
        out = requests.post(url=u, timeout=timeout, data=payload)
    except BaseException as e:
        description = "UNKNOWN - Unknown error: %s" % str(e)
        exit_code = 3
        return description, exit_code, token

    if out.status_code == 401:
        description = "CRITICAL - Invalid credentials"
        exit_code = 2
        return description, exit_code, token

    if out.status_code != 200:
        description = "WARNING - Unexpected status code %s" % out.status_code
        exit_code = 1
        return description, exit_code, token

    content = out.json()
    resp = content['Response']['data']

    if 'token' not in resp:
        description = "CRITICAL - Unable to get a valid authentication token"
        exit_code = 2
        return description, exit_code, token

    token = resp['token']

    description = "OK - Service reachable"
    exit_code = 0
    return description, exit_code, token


def checkLogout(URL, timeout, token):
    """ Check service authentication.
        Args:
           URL : service hostname
           timeout : how long should we wait for a response from the server
           token : authentication token received from login
    """

    u = URL + "/auth/logout"
    headers = {'Authorization': 'Bearer %s' % token}
    try:
        out = requests.get(url=u, timeout=timeout, headers=headers)
    except BaseException as e:
        description = "UNKNOWN - Unknown error: %s" % str(e)
        exit_code = 3
        return description, exit_code, token

    if out.status_code == 401:
        description = "CRITICAL - Invalid token"
        exit_code = 2
        return description, exit_code, token

    if out.status_code == 401:
        description = "CRITICAL - Invalid credentials"
        exit_code = 2
        return description, exit_code, token

    if out.status_code == 404:
        description = "CRITICAL - Endpoint not found"
        exit_code = 2
        return description, exit_code, token

    if out.status_code != 204:
        description = "WARNING - Unexpected status code %s" % out.status_code
        exit_code = 1
        return description, exit_code, token

    description = "OK - Service reachable"
    exit_code = 0
    return description, exit_code, token


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
    parser.add_argument("--user", "-u", metavar="user", help="User name to allow checks on authenticated endpoints")
    parser.add_argument("--password", "-P", metavar="password", help="Passoword to allow checks on authenticated endpoints")
    parser.add_argument("--verbose", "-v", dest='debug', help='Set verbosity level', action='count', default=0)
    arguments = parser.parse_args()
    ValidateValues(arguments)

    URL = arguments.hostname
    if arguments.port is not None:
        URL += ":%s" % arguments.port

    description, exit_code = checkHealth(URL, arguments.timeout)

    # Healt check failed, unable to continue
    if exit_code > 0:
        printResult(description, exit_code)

    # Authenticated tests not allowed, unable to continue
    if arguments.user is None or arguments.password is None:
        printResult(description, exit_code)

    description, exit_code, token = checkAuthentication(
        URL, arguments.timeout, arguments.user, arguments.password)

    # Authentication failed, unable to continue
    if exit_code > 0:
        printResult(description, exit_code)

    # No valid authentication token received, unable to continue
    if token is None:
        printResult(description, exit_code)

    description, exit_code, token = checkLogout(URL, arguments.timeout, token)

    printResult(description, exit_code)


if __name__ == "__main__":
    main()
