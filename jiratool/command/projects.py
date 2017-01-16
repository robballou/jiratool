from . import Cmd
from ..query import Query
import re

class AllCommand(Cmd):
    cmd = 'all'
    formatter = 'table.custom'

    @staticmethod
    def configure(parser):
        parser.add_argument('--filter', help='Regex for filtering projects')
        pass

    def filter_project(self, project, filter):
        if filter:
            if not re.search(filter, project.key, re.IGNORECASE) and not re.search(filter, project.name, re.IGNORECASE):
                return False
        return True

    def format_project(self, project, args):
        return {
            'key': project.key,
            'name': project.name,
        }

    def run(self, conf, args):
        projects = conf['jira'].projects()
        args.headers = ['Key', 'Name']
        args.row_keys = ['key', 'name']
        args.align = {'Key': 'l', 'Name': 'l'}
        return [self.format_project(project, args) for project in projects if self.filter_project(project, args.filter)]
