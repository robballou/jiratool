from os.path import dirname, basename, isfile
import glob
import importlib
import sys
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

class Cmd(object):
    formatter = None

    @staticmethod
    def configure(subparser):
        pass

    def error_message(self, message):
        sys.stderr.write("%s\n" % message)

    def get_project(self, conf, args):
        if args.project:
            return args.project
        if 'project' in conf:
            return conf['project']
        return False

command = {}
for item in __all__:
    if item[0] != '_':
        command[item] = importlib.import_module(".%s" % item, 'jiratool.command')
