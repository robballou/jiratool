from . import Cmd, OpenUrlCmd
from ..query import Query
from ..exceptions import JiraToolException, could_not_find_project
from ..configuration import get_status_flags, get
import subprocess
import shutil

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
        not_arg = 'not_%s' % flag.replace('-', '_')
        if arg in args and getattr(args, arg):
            q.add('status = "%s"' % flags[flag].name)
        if not_arg in args and getattr(args, not_arg):
            q.add('status != "%s"' % flags[flag].name)

def common_flags(conf, parser):
    """
    Add common flags for multiple commands.
    """
    parser.add_argument('--open', help='Only show issues with an open status', action='store_true', default=False)
    parser.add_argument('--any', '-a', help='Show issues for any project', action='store_true', default=False)

    flags = get_status_flags(conf)
    for flag in flags:
        parser.add_argument('--status-%s' % flag, help='Only show issues with the status "%s"' % flags[flag].name, default=False, action='store_true')
        parser.add_argument('--not-%s' % flag, help='Do not show issues with the status "%s"' % flags[flag].name, default=False, action='store_true')

class AllCommand(OpenUrlCmd):
    cmd = 'all'

    @classmethod
    def configure(cls, conf, parser):
        super().configure(conf, parser)
        common_flags(conf, parser)
        parser.add_argument('--assignee', help='Filter by assignee', default=None)
        parser.add_argument('--filter', help='Filter applied to the summary', default=None)

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project and not args.any:
            raise JiraToolException(could_not_find_project())

        q = Query()
        if project and not args.any:
            self.query_projects(conf, args, q, project)
        handle_common_filters(conf, args, q)
        if args.filter:
            q.add('summary ~ "%s"' % args.filter)
        return conf['jira'].search_issues("%s" % q)

class AttachmentsCommand(Cmd):
    cmd = 'attachments'
    formatter = 'yaml.basic'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('issue', help='The issue key(s) to get attachments from', nargs="+")
        parser.add_argument('--key', '-k', help="Only list a specific attachment")

    def run(self, conf, args):
        attachments = {}
        for issue_key in args.issue:
            issue = conf['jira'].issue(issue_key)
            attachments[issue_key] = []
            for attachment in issue.fields.attachment:
                if args.key and attachment.filename != args.key:
                    continue
                attachments[issue_key].append({'filename': attachment.filename, 'url': attachment.content})
        return attachments

class AssignCommand(Cmd):
    cmd = 'assign'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('assignee', help='User to assign to')
        parser.add_argument('issue', help='The issue key(s) to update', nargs="+")
        parser.add_argument('--comment', '-c', help="Add a comment to the issue(s)")

    def run(self, conf, args):
        for issue_key in args.issue:
            issue = conf['jira'].issue(issue_key)
            issue.update(assignee=args.assignee)
            if args.comment:
                conf['jira'].add_comment(issue_key, args.comment)
        return True

class CommentCommand(Cmd):
    cmd = 'comment'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('comment', help="The comment to add")
        parser.add_argument('issue', help="The issue key(s) to comment on", nargs="+")

    def run(self, conf, args):
        for issue in args.issue:
            conf['jira'].add_comment(issue, args.comment)

class DetailsCommand(Cmd):
    cmd = 'details'
    formatter = 'output.lines'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('issue', help='The issue key(s) to retrieve', nargs="+")

    def run(self, conf, args):
        size = shutil.get_terminal_size((80, 20))
        lines = []
        for issue in args.issue:
            this_issue = conf['jira'].issue(issue)
            lines.append('-' * size.columns)
            lines.append("%s: %s" % (issue, this_issue.fields.summary))
            lines.append('-' * size.columns)
            # for thing in this_issue.fields.__dict__:
            #     print(thing)
            lines.append('Status:\t\t%s' % this_issue.fields.status)
            lines.append('Assignee:\t%s' % this_issue.fields.assignee)
            lines.append('Updated:\t%s' % this_issue.fields.updated)
            if this_issue.fields.description:
                lines.append('-' * size.columns)
                lines.append(this_issue.fields.description)
            if this_issue.fields.issuelinks:
                lines.append('-' * size.columns)
                lines.append('LINKS')
                lines.append('-' * size.columns)
                for link in this_issue.fields.issuelinks:
                    try:
                        if getattr(link, 'inwardIssue'):
                            lines.append("* %s: %s: %s" % (link.type.inward, link.inwardIssue, link.inwardIssue.fields.summary))
                    except:
                        pass
                    try:
                        if getattr(link, 'outwardIssue'):
                            lines.append("* %s: %s: %s" % (link.type.outward, link.outwardIssue, link.outwardIssue.fields.summary))
                    except:
                        pass
            if this_issue.fields.attachment:
                lines.append('-' * size.columns)
                lines.append('ATTACHMENTS')
                lines.append('-' * size.columns)
                for attachment in this_issue.fields.attachment:
                    lines.append('- %s: %s' % (attachment.filename, attachment.content))

            if this_issue.fields.comment.comments:
                lines.append('-' * size.columns)
                lines.append('COMMENTS')
                lines.append('-' * size.columns)
                for comment in this_issue.fields.comment.comments:
                    this_comment = conf['jira'].comment(issue, comment)
                    print(this_comment.__dict__)
                    lines.append('Author:\t%s' % this_comment.author.name)
                    lines.append('Date:\t%s' % this_comment.created)
                    lines.append('\n')
                    lines.append(this_comment.body)
                    lines.append('-' * size.columns)
            lines.append("\n")
        return lines

class MineCommand(OpenUrlCmd):
    cmd = 'mine'

    @classmethod
    def configure(cls, conf, parser):
        super().configure(conf, parser)
        common_flags(conf, parser)
        parser.add_argument('--filter', help='Filter applied to the summary', default=None)
        if get(conf, 'options.custom_fields.epic_link'):
            parser.add_argument('--include-epic', help='Include epic', default=False, action="store_true")

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project and not args.any:
            raise JiraToolException(could_not_find_project())

        q = Query()
        if project and ('any' not in args or not args.any):
            self.query_projects(conf, args, q, project)
        q.add('assignee=currentUser()')
        handle_common_filters(conf, args, q)
        if args.filter:
            q.add('summary ~ "%s"' % args.filter)
        order_by = ['ID']
        if args.include_epic:
            order_by = ['"Epic Link"'] + order_by
        q = "%s ORDER BY %s" % (q, ', '.join(order_by))
        return conf['jira'].search_issues(q)

class UnassignedCommand(OpenUrlCmd):
    cmd = 'unassigned'

    @classmethod
    def configure(cls, conf, parser):
        super().configure(conf, parser)
        common_flags(conf, parser)
        parser.add_argument('--filter', help='Filter applied to the summary', default=None)

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project and not args.any:
            raise JiraToolException(could_not_find_project())

        q = Query()
        if project and not args.any:
            self.query_projects(conf, args, q, project)
        q.add('assignee IS EMPTY')
        handle_common_filters(conf, args, q)
        if args.filter:
            q.add('summary ~ "%s"' % args.filter)
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
        parser.add_argument('--comment', '-c', help="Add a comment to the issue(s)")

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
            if args.comment:
                conf['jira'].add_comment(issue_key, args.comment)
        return True

class TransitionsCommand(Cmd):
    cmd = 'transitions'
    formatter = 'table.custom'

    @classmethod
    def configure(cls, conf, parser):
        parser.add_argument('issue', help='The issue key(s) to update', nargs="+")

    def run(self, conf, args):
        rows = []
        for issue_key in args.issue:
            issue = conf['jira'].issue(issue_key)
            transitions = conf['jira'].transitions(issue)
            available_transitions = sorted([transition['name'] for transition in transitions])
            rows.append({'issue': issue_key, 'transitions': ', '.join(available_transitions)})

        args.headers = ['Issue', 'Transitions']
        args.align = {'Issue': 'l', 'Transitions': 'l'}
        args.row_keys = ['issue', 'transitions']
        return rows
