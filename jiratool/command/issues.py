from . import Cmd, OpenUrlCmd
from ..query import Query
from ..exceptions import JiraToolException
from ..configuration import get_status_flags
import subprocess

def handle_common_filters(conf, args, q):
    if 'assignee' in args and args.assignee:
        q.add('assignee=%s' % args.assignee)
    if args.open:
        query_string = []
        for status in conf['options']['status']['closed']:
            query_string.append('status != "%s"' % status)
        q.add(" AND ".join(query_string))

    flags = get_status_flags(conf)

    for flag in flags:
        arg = 'status_%s' % flag.replace('-', '_')
        if arg in args and getattr(args, arg):
            q.add('status = "%s"' % flags[flag].name)

def common_flags(conf, parser):
    parser.add_argument('--open', help='Only show issues with an open status', action='store_true', default=False)

    flags = get_status_flags(conf)
    for flag in flags:
        parser.add_argument('--status-%s' % flag, help='Only show issues with the status "%s"' % flags[flag].name, default=False, action='store_true')

class AllCommand(OpenUrlCmd):
    cmd = 'all'

    @classmethod
    def configure(cls, conf, parser):
        super().configure(conf, parser)
        common_flags(conf, parser)
        parser.add_argument('--assignee', help='Filter by assignee', default=None)

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project:
            raise JiraToolException('Could not find project in the command options or in configuration.')

        q = Query()
        q.add('project=%s' % project)
        handle_common_filters(conf, args, q)
        return conf['jira'].search_issues("%s" % q)

class AssignCommand(Cmd):
    cmd = 'assign'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('assignee', help='User to assign to')
        parser.add_argument('issue', help='The issue key(s) to update', nargs="+")

    def run(self, conf, args):
        for issue_key in args.issue:
            issue = conf['jira'].issue(args.issue)
            transitions = conf['jira'].transitions(issue)
            available_transitions = []
            transition_id = None
            for transition in transitions:
                available_transitions.append(transition['name'])
                if transition['name'] == args.status:
                    transition_id = transition['id']
                    break
            if not transition_id:
                self.error_message('Could not find transition to: %s. Available transitions: %s' % (args.status, ', '.join(available_transitions)))
                return False
            conf['jira'].transition_issue(issue, transition['id'])
        return True

class MineCommand(OpenUrlCmd):
    cmd = 'mine'

    @classmethod
    def configure(cls, conf, parser):
        super().configure(conf, parser)
        common_flags(conf, parser)

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project:
            raise JiraToolException('Could not find project')

        q = Query()
        q.add('project=%s' % project)
        q.add('assignee=currentUser()')
        handle_common_filters(conf, args, q)
        return conf['jira'].search_issues("%s" % q)

class OpenCommand(Cmd):
    cmd = 'open'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('issue', help='Open the issue URLs', nargs='+')

    def run(self, conf, args):
        for issue_key in args.issue:
            subprocess.run(['open', '%sbrowse/%s' % (conf['auth']['url'], issue_key)])
        return True

class StatusCommand(Cmd):
    cmd = 'status'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('status', help='Issue status to change it to')
        parser.add_argument('issue', help='The issue key(s) to update', nargs="+")

    def run(self, conf, args):
        for issue_key in args.issue:
            issue = conf['jira'].issue(issue_key)
            transitions = conf['jira'].transitions(issue)
            available_transitions = []
            transition_id = None
            for transition in transitions:
                available_transitions.append(transition['name'])
                if transition['name'] == args.status:
                    transition_id = transition['id']
                    break
            if not transition_id:
                self.error_message('Could not find transition to: %s. Available transitions: %s' % (args.status, ', '.join(available_transitions)))
                return False
            conf['jira'].transition_issue(issue, transition_id)
        return True
