import json

def ids(conf, args, results):
    print(json.dumps([item for item in map((lambda x: x.key), results)]))
