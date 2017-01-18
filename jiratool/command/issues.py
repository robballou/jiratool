from . import Cmd
from ..query import Query

def common_flags(parser):
    parser.add_argument('--open', help='Only open issues', action='store_true', default=False)
    parser.add_argument('--in-progress', help='Only in-progress issues', action='store_true', default=False)
    parser.add_argument('--client-review', help='Only client review issues', action='store_true', default=False)
    parser.add_argument('--internal-review', help='Only internal review issues', action='store_true', default=False)
    parser.add_argument('--truncate', help='Truncate the summary', default=50)

class AllCommand(Cmd):
    cmd = 'all'

    @staticmethod
    def configure(parser):
        common_flags(parser)
        parser.add_argument('--assignee', help='Filter by assignee', default=None)

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project:
            raise Exception('Could not find project in the command options or in configuration.')

        q = Query()
        q.add('project=%s' % project)
        q.add('assignee=%s' % args.assignee)
        if args.open:
            q.add('status != Closed AND status != Resolved')
        if args.in_progress:
            q.add('status != "In Progress"')
        if args.internal_review:
            q.add('status != "Internal Review"')
        if args.client_review:
            q.add('status != "Client Review"')
        return conf['jira'].search_issues("%s" % q)

class AssignCommand(Cmd):
    cmd = 'assign'

    @staticmethod
    def configure(parser):
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

class MineCommand(Cmd):
    cmd = 'mine'

    @staticmethod
    def configure(parser):
        common_flags(parser)

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project:
            raise Exception('Could not find project')

        q = Query()
        q.add('project=%s' % project)
        q.add('assignee=currentUser()')
        if args.open:
            q.add('status != Closed AND status != Resolved')
        if args.in_progress:
            q.add('status = "In Progress"')
        if args.internal_review:
            q.add('status = "Internal Review"')
        if args.client_review:
            q.add('status = "Client Review"')
        return conf['jira'].search_issues("%s" % q)

class StatusCommand(Cmd):
    cmd = 'status'

    @staticmethod
    def configure(parser):
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
