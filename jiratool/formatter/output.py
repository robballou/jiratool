import sys

def stderr(conf, args, results):
    sys.stderr.write(results)

def stdout(conf, args, results):
    sys.stdout.write(results)
