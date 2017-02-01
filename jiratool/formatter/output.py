import sys

def stderr(conf, args, results):
    sys.stderr.write(results)

def stdout(conf, args, results):
    if not isinstance(results, str):
        results = "%s" % results
    sys.stdout.write("%s\n" % results)

def lines(conf, args, results):
    for result in results:
        print(result)

def list(conf, args, results):
    print(', '.join(results))
