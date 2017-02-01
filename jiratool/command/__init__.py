from os.path import dirname, basename, isfile
import glob
import importlib
import sys
from ..query import Query

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

class Cmd(object):
    formatter = None

    @classmethod
    def configure(cls, conf, subparser):
        pass

    def error_message(self, message):
        sys.stderr.write("%s\n" % message)

    def get_project(self, conf, args):
        if args.project:
            if isinstance(args.project, str):
                args.project = (args.project,)
            return args.project
        if 'project' in conf:
            if isinstance(conf['project'], str):
                conf['project'] = (conf['project'],)
            return conf['project']
        return False

    def has_option(self, conf, args, option):
        if 'options' not in conf or args.cmd not in conf['options']:
            return None
        if option not in conf['options'][args.cmd]:
            return None
        return conf['options'][args.cmd][option]

    def has_options(self, conf, args):
        if 'options' in conf and args.cmd in conf['options']:
            return True

    def query_projects(self, conf, args, query, project):
        projects_query = Query(joiner='OR')
        for proj in project:
            projects_query.add('project=%s' % proj)
        query.add(projects_query)

    def update_args(self, conf, args):
        if self.has_options(conf, args):
            for arg in vars(args):
                opt = self.has_option(conf, args, arg)
                if opt != None:
                    setattr(args, arg, opt)

class OpenUrlCmd(Cmd):

    @classmethod
    def configure(cls, conf, subparser):
        subparser.add_argument('--open-url', '-o', help='Open the resulting URL', action='store_true')

command = {}
for item in __all__:
    if item[0] != '_':
        command[item] = importlib.import_module(".%s" % item, 'jiratool.command')
