from . import Cmd, OpenUrlCmd
from ..query import Query
import re
import warnings
import pprint

class AllCommand(Cmd):
    cmd = 'all'
    formatter = 'table.custom'

    @classmethod
    def configure(cls, conf, parser):
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

class DetailsCommand(Cmd):
    cmd = 'details'
    formatter = 'output.pretty'

    def run(self, conf, args):
        if not args.project:
            self.error_message('You must specify a project')
            return

        projects = []
        unique_projects = set(args.project)
        for project in unique_projects:
            jira_project = conf['jira'].project(project)
            projects.append(jira_project.__dict__)

        return projects

class SprintsCommand(Cmd):
    cmd = 'sprints'
    formatter = 'output.pretty'

    def run(self, conf, args):
        if not args.project:
            self.error_message('You must specify a project')
            return
        
        for project in args.project:
            project_board = get_project_board(project, conf)
            if project_board != None:
                sprints = conf['jira'].sprints(board_id=project_board.id)
                return sprints.__dict__
            self.error_message('No project board found for %s' % project)

class BoardCommand(OpenUrlCmd):
    cmd = 'board'
    formatter = 'table.custom'

    def run(self, conf, args):
        projects = self.get_project(conf, args)

        boards = []
        for project in projects:
            project = conf['jira'].project(project)
            args.headers = ['ID', 'Name', 'URL']
            args.row_keys = ['id', 'name', 'url']

            project_board = get_project_board(project, conf)

            if project_board != None:
                url = project_board._options['server'] + '/secure/RapidBoard.jspa?rapidView=%s' % project_board.id
                boards.append({'id': project_board.id, 'name': project_board.raw['name'], 'url': url})

        if boards:
            return boards
        self.error_message('Could not find project board')
        return False


def get_project_board(project, conf):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        project_boards = conf['jira'].boards()
    for board in project_boards:
        try:
            for board_project in board.filter.queryProjects.projects:
                if board_project.key == project.key:
                    print('Found board')
                    return board
        except:
            pass
    return None
