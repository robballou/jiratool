import json
from . import Cmd
from .. import configuration
from ..format import get_formatters

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
