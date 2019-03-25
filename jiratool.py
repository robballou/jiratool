#!/usr/bin/env python

from jira import JIRA
from jiratool import configuration
from jiratool import commands
from jiratool.format import get_formatter
from jiratool.exceptions import JiraToolException, CouldNotFindConfigurationFileException
import argparse
import sys
import getpass
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='JIRA Tools')
    parser.add_argument('--url', help='JIRA url', nargs=1)
    parser.add_argument('--username', help='JIRA username', nargs=1)
    parser.add_argument('--project', '-p', help='Project code', nargs="*")
    parser.add_argument('--formatter', '-f', help='Output formatter', default=None)
    parser.add_argument('--field', help='Specific fields', default=None)
    parser.add_argument('--json', help='Output in JSON. Same as --formatter=json.basic', action='store_true')
    parser.add_argument('--yaml', help='Output in YAML. Same as --formatter=yaml.basic', action='store_true')
    parser.add_argument('--no-defaults', '-n', help='Do not include default options from configuration files', default=False, action='store_true')
    parser.add_argument('--debug', '-d', help='Print debugging information', default=False, action='store_true')
    parser.add_argument('--no-truncation', help='Do not truncate in tables', default=False, action='store_true')

    config_args, remaining_args = parser.parse_known_args()

    auth = None
    url = None
    if config_args.url:
        url = config_args.url[0]
    elif 'JIRA_URL' in os.environ:
        url = os.environ['JIRA_URL']

    username = None
    if config_args.username:
        username = config_args.username[0]
    elif 'JIRA_USERNAME' in os.environ:
        username = os.environ['JIRA_USERNAME']

    password = None
    if 'JIRA_PASSWORD' in os.environ:
        password = os.environ['JIRA_PASSWORD']

    conf = {
        'auth': {
            'url': url,
        },
        'options': {
            'status': {
                'closed': ['done']
            }
        },
    }

    try:
        conf = configuration.load()
        auth = configuration.get_authentication(conf)
        url = conf['auth']['url']
    except CouldNotFindConfigurationFileException as e:
        # prompt for username/password
        if sys.stdin.isatty():
            try:
                if not url:
                    url = input('JIRA url: ')
                if not username:
                    username = input('Username: ')
                if not password:
                    password = getpass.getpass('Password: ')
                if username and password:
                    auth = (username, password)
            except KeyboardInterrupt:
                sys.stdout.write("\n")

    if not auth:
        sys.stderr.write("Error: Could not get configuration details\n")
        sys.exit(1)

    if not url.endswith("/"):
        url = "%s/" % url
    conf['auth']['url'] = url
    conf['jira'] = JIRA({ 'server': url }, basic_auth=auth)

    subparser = parser.add_subparsers()
    commands.configure_commands(conf, subparser)

    cmd_args = sys.argv[1:]
    if len(sys.argv) == 1 and 'default_command' in conf['options']:
        cmd_args = [conf['options']['default_command']]

    args = parser.parse_args(cmd_args)
    if 'cmd' not in args:
        parser.print_usage()
        sys.exit()

    try:
        (results, formatter) = commands.run_command(conf, args)
    except JiraToolException as e:
        sys.stderr.write("Error: %s\n" % e)
        if args.debug:
            raise e
        sys.exit(1)

    if results == None or results == False:
        sys.exit(1)

    if results == True:
        sys.exit()

    formatter = get_formatter(conf, args, formatter)
    formatter(conf, args, results)
