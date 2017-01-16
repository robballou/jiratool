#!/usr/bin/env python
from jira import JIRA
from jiratool import configuration
from jiratool import commands
from jiratool.format import get_formatter
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JIRA Tools')
    parser.add_argument('--project', '-p', help='Project code')
    parser.add_argument('--formatter', help='Output formatter', default=None)
    parser.add_argument('--no-defaults', '-n', help='Do not include default options from configuration files', default=False, action='store_true')

    subparser = parser.add_subparsers()
    commands.configure_commands(subparser)

    args = parser.parse_args()
    if 'cmd' not in args:
        parser.print_usage()
        sys.exit()

    conf = configuration.load()
    conf['jira'] = JIRA(conf['auth']['url'], basic_auth=configuration.get_authentication(conf))

    try:
        (results, formatter) = commands.run_command(conf, args)
    except Exception as e:
        sys.stderr.write("Error: %s\n" % e)
        sys.exit(1)

    if results == None or results == False:
        sys.exit(1)

    if results == True:
        sys.exit()

    formatter = get_formatter(conf, args, formatter)
    formatter(conf, args, results)
