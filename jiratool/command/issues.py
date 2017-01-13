from . import Cmd
from ..query import Query

class MineCommand(Cmd):
    cmd = 'mine'

    def run(self, conf, args):
        project = self.get_project(conf, args)
        if not project:
            raise Exception('Could not find project')

        q = Query()
        q.add('project=%s' % project)
        q.add('assignee=currentUser()')
        if args.open:
            q.add('status != Closed AND status != Resolved')
        return conf['jira'].search_issues("%s" % q)
