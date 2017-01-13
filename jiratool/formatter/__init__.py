from os.path import dirname, basename, isfile
import glob
import importlib
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

formatters = {}
for item in __all__:
    if item[0] != '_':
        formatters[item] = importlib.import_module(".%s" % item, 'jiratool.formatter')
