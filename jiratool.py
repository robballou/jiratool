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

    subparser = parser.add_subparsers()
    commands.configure_commands(subparser)

    args = parser.parse_args()

    conf = configuration.load()
    conf['jira'] = JIRA(conf['auth']['url'], basic_auth=configuration.get_authentication(conf))

    (results, formatter) = commands.run_command(conf, args)
    if results == None or results == False:
        sys.exit(1)

    if results == True:
        sys.exit()

    formatter = get_formatter(conf, args, formatter)
    formatter(conf, args, results)
