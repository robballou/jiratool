import json
from . import Cmd
from .. import configuration
from ..format import get_formatters
from ..configuration import get_status_names, get_status_flags

class ListCommand(Cmd):
    cmd = 'list'
    formatter = 'output.stdout'

    def run(self, conf, args):
        conf_copy = conf
        del conf_copy['jira']
        return json.dumps(conf_copy, indent=4)

class SourcesCommand(Cmd):
    cmd = 'sources'
    formatter = 'output.lines'

    def run(self, conf, args):
        return configuration.find_configuration_file()

class FormattersCommand(Cmd):
    cmd = 'formatters'
    formatter = 'output.lines'

    def run(self, conf, args):
        return get_formatters()

class StatusesCommand(Cmd):
    cmd = 'statuses'
    formatter = 'output.lines'

    def run(self, conf, args):
        return get_status_names(conf)

class StatusFlagsCommand(Cmd):
    cmd = 'status_flags'
    formatter = 'table.custom'

    def run(self, conf, args):
        args.headers = ['Flag', 'Status']
        flags = get_status_flags(conf)
        rows = []
        for flag in flags:
            rows.append({'flag': flag, 'name': flags[flag].name})
        args.row_keys = ['flag', 'name']
        args.align = {'Flag': 'l', 'Status': 'l'}
        return rows
