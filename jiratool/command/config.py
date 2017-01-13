import json
from . import Cmd
from .. import configuration

class ListCommand(Cmd):
    cmd = 'list'
    formatter = 'output.stdout'

    def run(self, conf, args):
        conf_copy = conf
        del conf_copy['jira']
        return json.dumps(conf_copy, indent=4)

class SourcesCommand(Cmd):
    cmd = 'sources'
    formatter = 'output.stdout'

    def run(self, conf, args):
        conf_copy = conf
        return "%s" % configuration.find_configuration_file()
