from . import Cmd
from ..query import Query
import re
import warnings

class AllCommand(Cmd):
    cmd = 'all'
    formatter = 'table.custom'

    @staticmethod
    def configure(parser):
        parser.add_argument('--filter', help='Regex for filtering projects')

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

class BoardCommand(Cmd):
    cmd = 'board'
    formatter = 'table.custom'

    @staticmethod
    def configure(parser):
        parser.add_argument('--open-url', '-o', help='Open the resulting URL', action='store_true')

    def run(self, conf, args):
        project = self.get_project(conf, args)
        project = conf['jira'].project(project)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            boards = conf['jira'].boards()

        args.headers = ['ID', 'Name', 'URL']
        args.row_keys = ['id', 'name', 'url']

        project_board = None
        for board in boards:
            try:
                for board_project in board.filter.queryProjects.projects:
                    if board_project.key == project.key:
                        project_board = board
                        break
            except:
                pass

        if project_board != None:
            url = project_board._options['server'] + '/secure/RapidBoard.jspa?rapidView=%s' % project_board.id
            return [{'id': project_board.id, 'name': project_board.raw['name'], 'url': url}]

        self.error_message('Could not find project board')
        return False
