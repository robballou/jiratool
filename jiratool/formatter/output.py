import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)

def pretty(conf, args, results):
    print(results)
    pp.pprint(results)

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

def field(conf, args, results):
    for issue in results:
        attachments = results[issue]
        for attachment in attachments:
            print(attachment[args.field])
