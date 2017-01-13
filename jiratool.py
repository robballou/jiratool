from jira import JIRA
from jiratool import configuration
from jiratool import commands
from jiratool.format import get_formatter
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JIRA Tools')
    parser.add_argument('command', nargs=1, help='Command to run')
    parser.add_argument('--project', '-p', help='Project code')
    parser.add_argument('--open', help='Only open issues', action='store_true', default=False)
    parser.add_argument('--formatter', help='Output formatter', default=None)
    args = parser.parse_args()

    conf = configuration.load()
    conf['jira'] = JIRA(conf['auth']['url'], basic_auth=configuration.get_authentication(conf))

    (results, formatter) = commands.run_command(conf, args)
    formatter = get_formatter(conf, args, formatter)
    formatter(conf, args, results)
