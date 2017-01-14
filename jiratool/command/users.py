from . import Cmd
from ..query import Query
import re

class ListCommand(Cmd):
    cmd = 'list'
    formatter = 'output.lines'

    @staticmethod
    def configure(parser):
        parser.add_argument('--filter', nargs='?')

    def run(self, conf, args):
        groups = conf['jira'].groups()
        users = []
        args.filter = re.compile('.*%s.*' % args.filter)
        for group in groups:
            group_users = conf['jira'].group_members(group)
            for user in group_users:
                if user in users:
                    continue
                if args.filter and not args.filter.search(group_users[user]['fullname']) and not args.filter.search(group_users[user]['email']):
                    continue
                users.append(user)
        users.sort()
        return users
        # users = conf['jira'].search_users('')
        # print(users)
